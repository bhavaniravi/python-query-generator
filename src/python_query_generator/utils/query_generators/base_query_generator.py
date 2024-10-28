from abc import ABC, abstractmethod
from typing import Any

from python_query_generator.schemas import Config


class BaseQueryGenerator(ABC):
	@abstractmethod
	def generate_query(self, config: Config) -> str | list[dict[str, Any]]:
		pass
