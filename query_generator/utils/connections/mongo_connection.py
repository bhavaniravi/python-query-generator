from collections.abc import Mapping
from typing import Any

from pymongo import MongoClient  # type: ignore
from pymongo.synchronous.database import Database  # type: ignore

from query_generator.utils.connections.base_connection import BaseConnection


class MongoConnection(BaseConnection):
	def __init__(self, connection_string: str, database_name: str):
		self.connection_string = connection_string
		self.database_name = database_name

	def connect(self) -> Database[Mapping[str, Any]]:
		client: MongoClient = MongoClient(self.connection_string)
		return client[self.database_name]
