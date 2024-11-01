from query_generator.schemas import QueryConfig
from query_generator.utils.query_generator_factory import QueryGeneratorFactory


class QueryGenerator:
	def __init__(self, db_type: str):
		self.query_generator_factory = QueryGeneratorFactory(db_type)

	def get_query(self, filter_config: QueryConfig):
		query_generator = self.query_generator_factory.get_query_generator()
		query = query_generator.generate_query(filter_config.config)
		return query
