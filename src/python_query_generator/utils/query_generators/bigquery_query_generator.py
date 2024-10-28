from python_query_generator.schemas import Config, SelectConfig
from python_query_generator.utils.query_generators.base_query_generator import (
	BaseQueryGenerator,
)


def format_value(value: SelectConfig | str | float | bool | list | None) -> str:
	if isinstance(value, str):
		return f"'{value}'"
	if value is None:
		return "NULL"
	if isinstance(value, list):
		return f"({', '.join(format_value(v) for v in value)})"
	return str(value)


class BigQueryQueryGenerator(BaseQueryGenerator):
	def generate_query(self, config: Config) -> str:
		fields: str = "*"
		if config.fields:
			fields = ", ".join([f.serialize_bigquery() for f in config.fields])

		source = config.source

		query = f"SELECT {fields} FROM `{source}`"  # noqa: S608

		for join in config.joins:
			conditions = f"{join.table}.{join.foreign_field} = {source}.{join.local_field}"
			query += f" JOIN `{join.table}` ON {conditions}"

		if config.filters:
			filter_conditions = " AND ".join(f"{f.field} {f.operator} {format_value(f.value)}" for f in config.filters)
			query += f" WHERE {filter_conditions}"

		if config.group:
			query += f" GROUP BY {', '.join(config.group.groupby_fields)}"

		if config.sort:
			sort_conditions = ", ".join(s.serialize_bigquery() for s in config.sort)
			query += f" ORDER BY {sort_conditions}"

		if config.limit:
			query += f" LIMIT {config.limit}"

		if config.offset:
			query += f" OFFSET {config.offset}"

		return query
