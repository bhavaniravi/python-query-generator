from query_generator.utils.query_generators.base_query_generator import (
	BaseQueryGenerator,
)


def format_value(value):
	if isinstance(value, str):
		return f"'{value}'"
	elif value is None:
		return "NULL"
	elif isinstance(value, list):
		return f"({', '.join(format_value(v) for v in value)})"
	return str(value)


class PostgresQueryGenerator(BaseQueryGenerator):
	def generate_query(self, config):
		source = config.source
		fields = ", ".join([f.serialize_postgres() for f in config.fields])

		query = f"SELECT {fields} FROM {source}"

		for join in config.joins:
			conditions = f"{join.table}.{join.foreign_field} = {source}.{join.local_field}"
			query += f" JOIN {join.table} ON {conditions}"

		if config.filters:
			filter_conditions = " AND ".join(f"{f.field} {f.operator} {format_value(f.value)}" for f in config.filters)
			query += f" WHERE {filter_conditions}"

		if config.group:
			query += f" GROUP BY {', '.join(config.group.groupby_fields)}"

		if config.sort:
			sort_conditions = ", ".join(s.serialize_postgres() for s in config.sort)
			query += f" ORDER BY {sort_conditions}"

		if config.limit:
			query += f" LIMIT {config.limit}"

		if config.offset:
			query += f" OFFSET {config.offset}"

		return query
