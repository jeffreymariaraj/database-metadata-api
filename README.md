# Database Metadata API

A FastAPI application that provides an API to retrieve metadata from database tables including column names, data types, constraints, and indexes.

## Features

- Retrieves metadata for all tables in a database
- Supports PostgreSQL, MySQL, and SQLite
- Uses SQLAlchemy for database interaction
- Configurable via environment variables
- Returns metadata as structured JSON
- Handles database connection errors gracefully

## Setup

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/database-metadata-api.git
cd database-metadata-api
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure the database connection:

```bash
cp .env.example .env
```

Edit the `.env` file to set your database connection string.

## Running the API

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Testing with Sample Data

To test the API with sample data:

1. Create a SQLite database with sample tables:

```bash
sqlite3 test_db.sqlite
```

2. Run the provided SQL statements from the [Sample Tables](#sample-tables) section below.

3. Set your database URL in the `.env` file:

```
DATABASE_URL="sqlite+aiosqlite:///./test_db.sqlite"
```

4. Start the API server:

```bash
uvicorn main:app --reload
```

## API Documentation

OpenAPI documentation is available at http://localhost:8000/docs

## API Endpoints

### GET /api/v1/tables

Returns a list of all table names in the configured database.

Example response:

```json
["users", "categories", "posts", "tags", "post_tags", "comments", "media", "sample_types", "settings"]
```

### GET /api/v1/metadata

Returns metadata for all tables in the configured database.

Example response:

```json
{
  "database_type": "sqlite",
  "tables": {
    "users": {
      "columns": [
        {
          "name": "id",
          "type": "INTEGER",
          "nullable": false,
          "default": "None",
          "autoincrement": true
        },
        {
          "name": "username",
          "type": "VARCHAR(50)",
          "nullable": false,
          "default": "None",
          "autoincrement": false
        },
        {
          "name": "email",
          "type": "VARCHAR(100)",
          "nullable": false,
          "default": "None",
          "autoincrement": false
        }
      ],
      "primary_key": ["id"],
      "foreign_keys": [],
      "indexes": [
        {
          "name": "ix_users_email",
          "columns": ["email"],
          "unique": true
        }
      ],
      "unique_constraints": [
        {
          "name": "uq_users_username",
          "columns": ["username"]
        }
      ]
    }
  }
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages for various error conditions, such as:

- 500 Internal Server Error: Database connection failures or metadata retrieval errors

## Sample Tables

Here are sample tables for testing the API with SQLite:

```sql
-- Users table with various constraints
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    CHECK (length(username) >= 3)
);

-- Create an index on the users email
CREATE INDEX idx_users_email ON users(email);

-- Categories for content organization
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    parent_id INTEGER,
    position INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- More tables and sample SQL statements can be found in the documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 