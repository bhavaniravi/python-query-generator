from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ConditionEnum(str, Enum):
	AND = "AND"
	OR = "OR"


class OperatorEnum(str, Enum):
	EQ = "EQ"
	NE = "NE"
	GT = "GT"
	LT = "LT"
	GTE = "GTE"
	LTE = "LTE"
	IN = "IN"
	NOT_IN = "NOT_IN"
	LIKE = "LIKE"
	NOT_LIKE = "NOT_LIKE"
	IS_NULL = "IS_NULL"
	IS_NOT_NULL = "IS_NOT_NULL"


class JoinTypeEnum(str, Enum):
	INNER = "INNER"
	LEFT = "LEFT"
	RIGHT = "RIGHT"
	FULL = "FULL"


class TransformationFunctionEnum(str, Enum):
	AVG = "AVG"
	SUM = "SUM"
	COUNT = "COUNT"
	MAX = "MAX"
	MIN = "MIN"
	FIRST = "FIRST"
	LAST = "LAST"
	CONCAT = "CONCAT"
	CONCAT_WS = "CONCAT_WS"
	UPPER = "UPPER"
	LOWER = "LOWER"
	TRIM = "TRIM"
	ROUND = "ROUND"
	FLOOR = "FLOOR"
	CEIL = "CEIL"
	ABS = "ABS"
	SQRT = "SQRT"
	EXP = "EXP"
	LN = "LN"
	LOG = "LOG"
	LOG10 = "LOG10"
	POW = "POW"
	POWER = "POWER"
	MOD = "MOD"
	SIN = "SIN"
	COS = "COS"
	TAN = "TAN"
	ASIN = "ASIN"
	ACOS = "ACOS"
	ATAN = "ATAN"
	ATAN2 = "ATAN2"


class DBEnum(str, Enum):
	POSTGRES = "POSTGRES"
	BIGQUERY = "BIGQUERY"
	MONGO = "MONGO"


class SelectConfig(BaseModel):
	field_name: str
	select_as: str | None = None
	transformation_function: str | None = None

	def serialize_postgres(self) -> str:
		"""
		Serialize the field for PostgresSQL.

		Returns:
			str: Serialized field with optional transformation function or alias.

		"""
		value = self.field_name
		if self.transformation_function:
			if self.transformation_function.upper() in ["YEAR", "MONTH", "DAY"]:
				value = f"extract({self.transformation_function.upper()} from {self.field_name})"
			else:
				value = f"{self.transformation_function}({self.field_name})"
		return value if not self.select_as else f"{value} as {self.select_as}"

	def serialize_bigquery(self) -> str:
		"""
		Serialize the field for BigQuery.

		Returns:
			str: Serialized field with optional transformation function or alias.

		"""
		if self.transformation_function:
			return (
				f"{self.transformation_function}({self.field_name})" + f" as {self.select_as}" if self.select_as else ""
			)

		return f"{self.field_name} as {self.select_as}" if self.select_as else self.field_name

	def serialize_mongo(self) -> dict[str, Any]:
		"""
		Serialize the field for MongoDB.

		Returns:
			dict[str, Any]: MongoDB serialization with optional transformation function or alias.

		Example:
			With transformation:
			{"full_name": {"$transformation_function": "$name"}}

			Without transformation:
			{"name": "$name"}

		"""
		if not self.select_as:
			self.select_as = self.field_name
		if self.transformation_function:
			return {self.select_as: {self.transformation_function: f"${self.field_name}"}}

		return {self.select_as: f"${self.field_name}"}


class SortConfig(BaseModel):
	field: str
	direction: str = "ASC"

	def serialize_postgres(self) -> str:
		"""
		Serialize the sorting configuration for PostgreSQL.

		Returns:
			str: Sorting direction (`ASC` or `DESC`) applied to the field.

		"""
		return f"{self.field} {self.direction}"

	def serialize_bigquery(self) -> str:
		"""
		Serialize the sorting configuration for BigQuery.

		Returns:
			str: Sorting direction (`ASC` or `DESC`) applied to the field.

		"""
		return f"{self.field} {self.direction}"

	def serialize_mongo(self) -> dict[str, Any]:
		"""
		Serialize the sorting configuration for MongoDB.

		Returns:
			dict[str, Any]: MongoDB sorting configuration (1 for `ASC`, -1 for `DESC`).

		Example:
			{"name": 1}  # ASC
			{"name": -1}  # DESC

		"""
		return {self.field: 1 if self.direction == "ASC" else -1}


class ConditionConfig(BaseModel):
	conjunction: str = "AND"
	conditions: list["FilterConfig"]


class JoinConfig(BaseModel):
	table: str
	join_type: str = "INNER"
	foreign_field: str
	local_field: str
	filters: list["FilterConfig"] = []


class FilterConfig(BaseModel):
	field: str = Field(..., min_length=1, max_length=100)
	operator: str = Field(..., min_length=1, max_length=10)
	value: SelectConfig | str | int | float | bool | list | None = None


class GroupConfig(BaseModel):
	groupby_fields: list[str]
	aggregate_fields: list[SelectConfig]


class Config(BaseModel):
	fields: list[SelectConfig] | None = None
	source: str
	filters: list[FilterConfig] | None = None
	group: GroupConfig | None = None
	sort: list[SortConfig] | None = None
	limit: int | None = None
	offset: int | None = None
	joins: list[JoinConfig] = []


class QueryConfig(BaseModel):
	name: str = Field(..., min_length=4, max_length=100)
	config: Config
