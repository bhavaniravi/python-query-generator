import json

from query_generator import QueryGenerator
from query_generator.schemas import QueryConfig


class TestMongoQueryGenerator:
	@classmethod
	def setup_class(cls):
		cls.query_service = QueryGenerator("mongodb")

	def test_run_query(self):
		filter_data = {
			"name": "test_filter",
			"config": {
				"fields": [
					{"field_name": "name"},
					{"field_name": "age"},
				],
				"source": "users",
			},
		}
		filter_data = QueryConfig(**filter_data)
		result = self.query_service.get_query(filter_data)
		assert result == [{"$project": {"name": "$name", "age": "$age"}}]

	def test_run_query_with_joins(self):
		filter_data = {
			"name": "test_filter",
			"config": {
				"fields": [
					{"field_name": "name"},
					{"field_name": "age"},
					{"field_name": "department_name", "select_as": "department"},
				],
				"source": "users",
				"joins": [
					{
						"table": "departments",
						"foreign_field": "id",
						"local_field": "users.department_id",
						"filters": [
							{
								"field": "users.department_id",
								"operator": "=",
								"value": "departments.id",
							}
						],
					}
				],
				"filters": [
					{
						"field": "age",
						"operator": ">",
						"value": 18,
						"type": "int",
					},
					{
						"field": "name",
						"operator": "=",
						"value": "John",
						"type": "str",
					},
				],
			},
		}
		filter_data = QueryConfig(**filter_data)
		result = self.query_service.get_query(filter_data)
		assert json.dumps(result, sort_keys=True) == json.dumps(
			[
				{
					"$project": {
						"name": "$name",
						"age": "$age",
						"department": "$department_name",
					}
				},
				{
					"$match": {
						"$and": [
							{"age": {"$gt": 18}},
							{"name": {"$eq": "John"}},
						]
					}
				},
				{
					"$lookup": {
						"as": "departments",
						"foreignField": "id",
						"from": "departments",
						"localField": "users.department_id",
					}
				},
			],
			sort_keys=True,
		)

	def test_groupby_and_sort(self):
		filter_data = {
			"name": "test_filter",
			"config": {
				"fields": [
					{"field_name": "department_name"},
					{
						"field_name": "age",
						"transformation_function": "avg",
						"select_as": "avg_age",
					},
				],
				"source": "users",
				"group": {
					"groupby_fields": ["department_name"],
					"aggregate_fields": [
						{
							"field_name": "age",
							"transformation_function": "avg",
							"select_as": "avg_age",
						}
					],
				},
				"sort": [{"field": "avg_age", "direction": "desc"}],
			},
		}
		filter_data = QueryConfig(**filter_data)
		result = self.query_service.get_query(filter_data)
		assert result == [
			{
				"$project": {
					"department_name": "$department_name",
					"avg_age": {"avg": "$age"},
				}
			},
			{
				"$group": {"_id": {"department_name": "$department_name"}},
			},  # noqa
			{
				"$sort": {"avg_age": -1},
			},
		]
