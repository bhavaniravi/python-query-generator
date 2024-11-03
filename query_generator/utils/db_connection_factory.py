from query_generator.config.settings import Settings
from query_generator.utils.connections.bigquery_connection import BigQueryConnection
from query_generator.utils.connections.mongo_connection import MongoConnection
from query_generator.utils.connections.postgres_connection import PostgresConnection


class DBConnectionFactory:
	def __init__(self, db_type: str, settings: Settings):
		self.db_type = db_type
		self.settings = settings

	def get_connection(self):
		if self.db_type == "postgresql":
			return PostgresConnection(self.settings.DATABASE_URL).connect()
		elif self.db_type == "mongodb":
			return MongoConnection(self.settings.MONGODB_URL, self.settings.MONGODB_DATABASE).connect()
		elif self.db_type == "bigquery":
			return BigQueryConnection(self.settings.GCP_CREDENTIALS_PATH).connect()
		else:
			raise ValueError(f"Unsupported database type: {self.db_type}")
