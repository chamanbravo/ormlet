import sqlite3

from ormlet.model import Model


class ConnectionManager:
    def __init__(self, db):
        self.db = db

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(
            self.db,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.connection.close()


class DatabaseManager:
    def __init__(self, sqlite_db: str):
        self._connection_manager = ConnectionManager(sqlite_db)

    def connect(self):
        return self._connection_manager

    def register_tables(self, tables: list[Model]):
        with self._connection_manager as connection:
            for table in tables:
                cursor = connection.cursor()
                cursor.execute(table.get_table_schema())
            connection.commit()
