from .query_generators.bigquery_query_generator import BigQueryQueryGenerator
from .query_generators.mongo_query_generator import MongoQueryGenerator
from .query_generators.postgres_query_generator import PostgresQueryGenerator


class QueryGeneratorFactory:
	def __init__(self, db_type: str):
		self.db_type = db_type

	def get_query_generator(self) -> PostgresQueryGenerator | MongoQueryGenerator | BigQueryQueryGenerator:
		if self.db_type == "postgresql":
			return PostgresQueryGenerator()
		if self.db_type == "mongodb":
			return MongoQueryGenerator()
		if self.db_type == "bigquery":
			return BigQueryQueryGenerator()
		value_error = f"Unsupported database type: {self.db_type}"
		raise ValueError(value_error)
