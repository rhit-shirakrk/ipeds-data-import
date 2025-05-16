"""
Creates MySQL tables from Microsoft Access DB tables
"""

import logging


class TableCreator:
    """
    Get table schematics from a Microsoft Access DB file, then create a
    representation of that table in Python
    """

    FALLBACK_PRIMARY_KEY_NAME = "fallback_rowid"
    FALLBACK_PRIMARY_KEY_DATATYPE = "INTEGER"
    ESCAPE_IDENTIFIER = "`"

    def __init__(self, access_db_cursor, mysql_cursor, win32_db) -> None:
        self.logger = logging.getLogger(__name__)
        self.access_db_cursor = access_db_cursor
        self.mysql_cursor = mysql_cursor
        self.win32_db = win32_db

    def generate_create_table_query(self, table_name: str) -> str:
        """Generate a MySQL query to create a Microsoft Access DB table in MySQL

        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: MySQL query to create the table
        :rtype: str
        """
        print(f"Creating table {table_name}")
        missing_primary_keys = False
        primary_keys = self._get_primary_keys(table_name)
        if not primary_keys:
            missing_primary_keys = True
            primary_keys = [f"{TableCreator.ESCAPE_IDENTIFIER}{TableCreator.FALLBACK_PRIMARY_KEY_NAME}{TableCreator.ESCAPE_IDENTIFIER}"]
            
        column_parameters = self._get_column_parameters(table_name)

        # add auto-incrementing id if there's no primary key
        if missing_primary_keys:
            column_parameters.append(f"{TableCreator.ESCAPE_IDENTIFIER}{TableCreator.FALLBACK_PRIMARY_KEY_NAME}{TableCreator.ESCAPE_IDENTIFIER} {TableCreator.FALLBACK_PRIMARY_KEY_DATATYPE} AUTO_INCREMENT")
        column_parameters.append(
            f"PRIMARY KEY ({', '.join(primary_keys)})"
        )
        column_parameters = ", ".join(column_parameters)
        return f"DROP TABLE IF EXISTS {table_name};\nCREATE TABLE {table_name}({column_parameters});"

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
                return [f"{TableCreator.ESCAPE_IDENTIFIER}{fld.Name}{TableCreator.ESCAPE_IDENTIFIER}" for fld in i.Fields]
            
    def _get_column_parameters(self, table_name: str) -> list[str]:
        """Generate all column parameters associated with a table

        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: The column parameters in a table
        :rtype: list[str]
        """
        column_parameters = []
        for row in self.access_db_cursor.columns(table=table_name):
            column_parameter = f"{TableCreator.ESCAPE_IDENTIFIER}{row.column_name}{TableCreator.ESCAPE_IDENTIFIER} {self._convert_to_mysql_datatype(row.type_name)}"
            if row.type_name == "VARCHAR":
                column_parameter += f"({row.column_size})"

            column_parameters.append(column_parameter)

        return column_parameters
    
    def _convert_to_mysql_datatype(self, column_type: str) -> str:
        """Convert a potentially-invalid column type to one used in MySQL

        :param column_type: The column type
        :type column_type: str
        :return: An equivalent, MySQL-compliant column type
        :rtype: str
        """
        match column_type:
            case "LONGCHAR":
                return "LONGTEXT"
            case _:
                return column_type