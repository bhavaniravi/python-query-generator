from python_query_generator.utils.connections.base_connection import BaseConnection
from sqlalchemy import Connection, create_engine


class PostgresConnection(BaseConnection):
	def __init__(self, database_url: str):
		self.database_url = database_url

	def connect(self) -> Connection:
		engine = create_engine(self.database_url)
		return engine.connect()