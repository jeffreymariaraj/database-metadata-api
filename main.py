from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

from app.database import get_db
from app.routers import metadata

app = FastAPI(
    title="Database Metadata API",
    description="API for retrieving metadata from database tables",
    version="0.1.0"
)

app.include_router(metadata.router, prefix="/api/v1", tags=["metadata"])

@app.get("/")
async def root():
    return {
        "message": "Database Metadata API",
        "docs_url": "/docs",
        "tables_endpoint": "/api/v1/tables",
        "metadata_endpoint": "/api/v1/metadata"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 