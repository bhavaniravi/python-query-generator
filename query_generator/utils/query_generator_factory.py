from query_generator.utils.query_generators.postgres_query_generator import (
    PostgresQueryGenerator,
)
from query_generator.utils.query_generators.mongo_query_generator import (
    MongoQueryGenerator,
)
from query_generator.utils.query_generators.bigquery_query_generator import (
    BigQueryQueryGenerator,
)


class QueryGeneratorFactory:
    def __init__(self, db_type: str):
        self.db_type = db_type

    def get_query_generator(self):
        if self.db_type == "postgresql":
            return PostgresQueryGenerator()
        elif self.db_type == "mongodb":
            return MongoQueryGenerator()
        elif self.db_type == "bigquery":
            return BigQueryQueryGenerator()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
