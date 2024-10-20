from sqlalchemy import create_engine
from query_generator.utils.connections.base_connection import BaseConnection


class PostgresConnection(BaseConnection):
    def __init__(self, database_url: str):
        self.database_url = database_url

    def connect(self):
        engine = create_engine(self.database_url)
        return engine.connect()
