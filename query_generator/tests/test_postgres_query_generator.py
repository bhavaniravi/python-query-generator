from query_generator import QueryGenerator
from query_generator.schemas import QueryConfig


class TestPostgresQueryGenerator:
    @classmethod
    def setup_class(cls):
        cls.query_service = QueryGenerator("postgresql")

    def test_query(self):
        filter_data = {
            "name": "test_filter",
            "config": {
                "source": "users",
                "fields": [
                    {"field_name": "name"},
                    {"field_name": "age"},
                ],
            },
        }
        filter_data = QueryConfig(**filter_data)
        result = self.query_service.get_query(filter_data)
        assert result == "SELECT name, age FROM users"

    def test_run_query_with_joins(self):
        filter_data = {
            "name": "test_filter",
            "config": {
                "fields": [
                    {"field_name": "name"},
                    {"field_name": "age"},
                    {"field_name": "department_name", "select_as": "department"},
                ],
                "source": "users",
                "joins": [
                    {
                        "table": "departments",
                        "foreign_field": "id",
                        "local_field": "department_id",
                    }
                ],
                "filters": [
                    {
                        "field": "age",
                        "operator": ">",
                        "value": 18,
                        "type": "int",
                    },
                    {
                        "field": "name",
                        "operator": "=",
                        "value": "John",
                        "type": "str",
                    },
                ],
            },
        }
        filter_data = QueryConfig(**filter_data)
        result = self.query_service.get_query(filter_data)
        assert (
            result.lower()
            == "SELECT name, age, department_name as department FROM users JOIN departments ON departments.id = users.department_id WHERE age > 18 and name = 'John'".lower()
        )

    def test_groupby_and_sort(self):
        filter_data = {
            "name": "test_filter",
            "config": {
                "fields": [
                    {"field_name": "department_name"},
                    {
                        "field_name": "age",
                        "transformation_function": "avg",
                        "select_as": "avg_age",
                    },
                ],
                "source": "users",
                "group": {
                    "groupby_fields": ["department_name"],
                    "aggregate_fields": [
                        {
                            "field_name": "age",
                            "transformation_function": "avg",
                            "select_as": "avg_age",
                        }
                    ],
                },
                "sort": [{"field": "avg_age", "direction": "desc"}],
            },
        }
        filter_data = QueryConfig(**filter_data)
        result = self.query_service.get_query(filter_data)
        assert (
            result.lower()
            == "SELECT department_name, avg(age) as avg_age FROM users GROUP BY department_name ORDER BY avg_age desc".lower()
        )

    def test_run_query_with_filter_datetme(self):
        filter_data = {
            "name": "test_filter",
            "config": {
                "fields": [
                    {"field_name": "name"},
                    {"field_name": "age"},
                    {"field_name": "department_name", "select_as": "department"},
                ],
                "source": "users",
                "filters": [
                    {
                        "field": "joined_on",
                        "operator": ">=",
                        "value": "2022-10-02 12:00:00",
                        "type": "datetime",
                    },
                    {
                        "field": "joined_on",
                        "operator": "<=",
                        "value": "2023-10-02 12:00:00",
                        "type": "datetime",
                    },
                ],
            },
        }
        filter_data = QueryConfig(**filter_data)
        result = self.query_service.get_query(filter_data)
        assert (
            result.lower()
            == "SELECT name, age, department_name as department FROM users WHERE joined_on >= '2022-10-02'".lower()
        )
