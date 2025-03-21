from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Any
from sqlalchemy import text

from app.database import get_db, get_inspector

router = APIRouter()

@router.get("/tables", response_model=List[str])
async def get_table_names(db: AsyncSession = Depends(get_db)):
    """
    Get a list of all table names in the database.
    
    Returns:
        List of table names.
    """
    try:
        # For SQLite specifically
        query = text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        result = await db.execute(query)
        tables = [row[0] for row in result.fetchall()]
        return tables
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving table names: {str(e)}"
        )

@router.get("/metadata", response_model=Dict[str, Any])
async def get_database_metadata(db: AsyncSession = Depends(get_db)):
    """
    Retrieve metadata for all tables in the database.
    
    Returns:
        Dict with tables and their metadata including columns, constraints, and indexes.
    """
    try:
        # Get table names using the same method as get_table_names
        query = text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        result = await db.execute(query)
        table_names = [row[0] for row in result.fetchall()]
        
        result_dict = {
            "database_type": "sqlite",
            "tables": {}
        }
        
        # Get metadata for each table
        for table_name in table_names:
            table_metadata = {
                "columns": [],
                "primary_key": [],
                "foreign_keys": [],
                "indexes": [],
                "unique_constraints": []
            }
            
            # Get column information
            columns_query = text(f"PRAGMA table_info({table_name})")
            columns_result = await db.execute(columns_query)
            columns = columns_result.fetchall()
            
            for column in columns:
                column_info = {
                    "name": column[1],  # column name
                    "type": column[2],  # data type
                    "nullable": not column[3],  # notnull
                    "default": column[4],  # dflt_value
                    "primary_key": bool(column[5])  # pk
                }
                table_metadata["columns"].append(column_info)
                if column[5]:  # If primary key
                    table_metadata["primary_key"].append(column[1])
            
            # Get foreign key information
            fk_query = text(f"PRAGMA foreign_key_list({table_name})")
            fk_result = await db.execute(fk_query)
            fks = fk_result.fetchall()
            
            for fk in fks:
                fk_info = {
                    "id": fk[0],
                    "seq": fk[1],
                    "table": fk[2],
                    "from": fk[3],
                    "to": fk[4],
                    "on_update": fk[5],
                    "on_delete": fk[6],
                    "match": fk[7]
                }
                table_metadata["foreign_keys"].append(fk_info)
            
            # Get index information
            idx_query = text(f"PRAGMA index_list({table_name})")
            idx_result = await db.execute(idx_query)
            indexes = idx_result.fetchall()
            
            for idx in indexes:
                index_name = idx[1]
                idx_col_query = text(f"PRAGMA index_info({index_name})")
                idx_col_result = await db.execute(idx_col_query)
                idx_columns = [col[2] for col in idx_col_result.fetchall()]
                
                index_info = {
                    "name": index_name,
                    "unique": bool(idx[2]),
                    "columns": idx_columns
                }
                table_metadata["indexes"].append(index_info)
            
            # Add table metadata to result
            result_dict["tables"][table_name] = table_metadata
        
        return result_dict
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving metadata: {str(e)}"
        ) 