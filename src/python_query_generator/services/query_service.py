from typing import Any

from src.python_query_generator.schemas import Config, QueryConfig
from src.python_query_generator.utils import QueryGeneratorFactory


class QueryGenerator:
	def __init__(self, db_type: str):
		self.query_generator_factory = QueryGeneratorFactory(db_type)

	def get_query(self, filter_config: QueryConfig | dict[str, Any]) -> str | list[dict[str, Any]]:
		query_generator = self.query_generator_factory.get_query_generator()
		if isinstance(filter_config, dict):
			filter_config = Config(**filter_config)
		return query_generator.generate_query(filter_config.config)
