# Python Query Generator

This project centralizes a JSON schema for filter configuration on the frontend, allowing direct serialization into backend queries. 

> **Note:** This project is under active development and is not ready for production use.

## Features & To-Do

- [x] Basic JSON schema for filters using Pydantic.
- [x] Query generation for PostgreSQL, MongoDB, and BigQuery.
- [ ] Advanced queries (complex transformations, aggregations).
- [ ] ID-based transformation for field mapping.
- [ ] Additional database support (Elasticsearch, Snowflake, Redshift).
- [ ] Complex filter types (date range, number range).
- [ ] Logical filter operations (AND, OR, NOT).

### Technical Debt
- [ ] Refactor query generation to be part of the Pydantic model for maintainability and clarity.

## Installation with `uv`

The `uv` package manager, known for its speed and Rust-based efficiency, is required to set up this project. You can install `uv` by following one of these methods:

- **Linux/macOS**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **macOS via Homebrew**:
  ```bash
  brew install uv
  ```
- **Windows**:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Using Pip** (alternative method):
  ```bash
  pip install uv
  ```

Once installed, verify by checking the version:
```bash
uv --version
```

## Setting Up the Project

1. **Setting up virtual environment**:
   ```bash
   uv sync
   ```

2. **Activate the Environment**:
   - **Linux/macOS**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows**:
     ```powershell
     .\.venv\Scripts\activate
     ```

## Usage

To use the `python-query-generator`, you can initialize the `QueryGenerator` class and pass a JSON filter configuration:

```python
from src.python_query_generator.services.query_service import QueryGenerator

query = {
    "filters": [
        {
            "field": "name",
            "operation": "eq",
            "value": "John Doe"
        }
    ]
}

query_generator = QueryGenerator(db_type="postgresql")
print(query_generator.get_query(query))
```
