# Python Query Generator

This project is built to have a centralized JSON schema for filter configuration on the front-end that can be directly serialized into a query on the backend.

This project is a work in progress and is not yet ready for production use.

## Todo

- [x] Create a basic JSON schema using pydantic
- [x] Create a basic query generator for postgres, mongo and bigquery
- [ ] Add support for more complex queries
- [ ] Id based transformation field mapping
- [ ] Add support for more databases (elasticsearch, snowflake, redshift)
- [ ] Add support for more complex filter types (date range, number range, etc)
- [ ] Add support for more complex filter operations (AND, OR, NOT)

### Tech Debt

- [ ] Rewrite the query generator as a part of the pydantic model. I believe this will make the code more maintainable and easier to understand.

## Installation

```bash
pip install query-generator
```

## Usage

```python

from query_generator import QueryGenerator

query = {
    "filters": [
        {
            "field": "name",
            "operation": "eq",
            "value": "John Doe"
        }
    ]
}

query_generator = QueryGenerator()
query_generator.generate_query(query)

```
