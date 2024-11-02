from query_generator.utils.query_generators.base_query_generator import (
    BaseQueryGenerator,
)


class MongoQueryGenerator(BaseQueryGenerator):
    def generate_query(self, config):
        pipeline = []

        fields = config.fields
        if fields:
            projection = {}
            for field in fields:
                projection.update(field.serialize_mongo())
            pipeline.append({"$project": projection})

        filters = config.filters
        if filters:
            filter_conditions = []
            for f in filters:
                field, operator, value = f.field, f.operator, f.value
                mongo_operator = {
                    "=": "$eq",
                    "!=": "$ne",
                    ">": "$gt",
                    "<": "$lt",
                    ">=": "$gte",
                    "<=": "$lte",
                    "IN": "$in",
                    "NOT IN": "$nin",
                }.get(operator, "$eq")
                filter_conditions.append({field: {mongo_operator: value}})
            filter_conditions = {"$and": filter_conditions}
            pipeline.append({"$match": filter_conditions})

        joins = config.joins
        for join in joins:
            lookup_pipeline = []
            lookup_stage = {
                "from": join.table,
                "localField": join.local_field,
                "foreignField": join.foreign_field,
                "as": join.table,
            }

            if len(join.filters) > 1:
                additional_conditions = {
                    "$match": {field: value for field, value in join.filters[1].items()}
                }
                lookup_pipeline.append(additional_conditions)
                lookup_stage["pipeline"] = lookup_pipeline

            pipeline.append({"$lookup": lookup_stage})

        group = config.group
        if group:
            group_stage = {
                "$group": {
                    "_id": {field: f"${field}" for field in group.groupby_fields}
                },
                "doc": {
                        "$first": "$$ROOT"
                }
            }
            pipeline.append(group_stage)
            pipeline.append({"$replaceRoot": {"newRoot": "$doc"}}) # Replace root with the original document
        sort = config.sort
        if sort:
            sort_stage = {
                "$sort": {
                    key: value
                    for s in sort
                    for key, value in s.serialize_mongo().items()
                }
            }
            pipeline.append(sort_stage)

        if "limit" in config:
            pipeline.append({"$limit": config["limit"]})

        if "offset" in config:
            pipeline.append({"$skip": config["offset"]})

        return pipeline
