from collections.abc import Mapping
from typing import Any

from connections.bigquery_connection import BigQueryConnection
from connections.mongo_connection import MongoConnection
from connections.postgres_connection import PostgresConnection
from google.cloud.bigquery import Client  # type: ignore
from pymongo.synchronous.database import Database  # type: ignore
from python_query_generator.config import Settings
from sqlalchemy import Connection  # type: ignore


class DBConnectionFactory:
	def __init__(self, db_type: str, settings: Settings):
		self.db_type = db_type
		self.settings = settings

	def get_connection(self) -> Connection | Database[Mapping[str, Any]] | Client:
		if self.db_type == "postgresql":
			return PostgresConnection(self.settings.DATABASE_URL).connect()
		if self.db_type == "mongodb":
			return MongoConnection(self.settings.MONGODB_URL, self.settings.MONGODB_DATABASE).connect()
		if self.db_type == "bigquery":
			return BigQueryConnection(self.settings.GCP_CREDENTIALS_PATH).connect()
		value_error: str = f"Unsupported database type: {self.db_type}"
		raise ValueError(value_error)
