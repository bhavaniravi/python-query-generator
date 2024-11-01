from google.cloud import bigquery

from query_generator.utils.connections.base_connection import BaseConnection


class BigQueryConnection(BaseConnection):
	def __init__(self, credentials_path: str):
		self.credentials_path = credentials_path

	def connect(self):
		return bigquery.Client.from_service_account_json(self.credentials_path)
