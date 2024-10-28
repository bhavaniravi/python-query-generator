from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from google.cloud.bigquery import Client
from pymongo.synchronous.database import Database
from sqlalchemy import Connection


class BaseConnection(ABC):
	@abstractmethod
	def connect(self) -> Client | Connection | Database[Mapping[str, Any]]:
		pass
