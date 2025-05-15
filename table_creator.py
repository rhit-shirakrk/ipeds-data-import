"""
Creates MySQL tables from Microsoft Access DB tables
"""

import logging


class TableCreator:
    """
    Get table schematics from a Microsoft Access DB file, then create a
    representation of that table in Python
    """

    def __init__(self, access_db_cursor, mysql_conn, win32_db) -> None:
        self.logger = logging.getLogger(__name__)
        self.access_db_cursor = access_db_cursor
        self.mysql_conn = mysql_conn
        self.win32_db = win32_db

    def create_table(self, table_name: str) -> None:
        """Create a table using the given table name

        :param table_name: The name of the table to create in Python
        :type table_name: str
        """
        column_parameters = [
            f"{row.column_name} {row.type_name}"
            for row in self.access_db_cursor.columns(table=table_name)
        ]
        column_parameters.append(
            f"PRIMARY KEY ({', '.join(self._get_primary_keys(table_name))})"
        )
        
        cursor = self.mysql_conn.cursor()
        cursor.execute(f"CREATE TABLE {table_name}({', '.join(column_parameters)})")
        cursor.close()
        self.logger.info(f"Successfully created table {table_name}\n")
        self.logger.info(f"Schematic:\nCREATE TABLE {table_name}({', '.join(column_parameters)})\n")

    def _get_primary_keys(self, table_name: str) -> list[str]:
        """Get primary keys associated with a table

        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: The primary keys in a table
        :rtype: list[str]
        """
        tbd = self.win32_db.TableDefs(table_name)
        for i in tbd.Indexes:
            if i.Primary:
                return [fld.Name for fld in i.Fields]
