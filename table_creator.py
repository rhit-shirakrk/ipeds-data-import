"""
Creates MySQL tables from Microsoft Access DB tables
"""

import logging
import pyodbc
import typing

class TableCreator:
    """Get table schematics from a Microsoft Access DB file, then create a
    representation of that table in Python

    :param access_db_cursor: Access point into the Microsoft Access DB file
    :type access_db_cursor: pyodbc.Cursor
    :param win32_db: Access point (with Windows API) into the Microsoft Access DB file
    :type win32_db: typing.Any
    """

    FALLBACK_PRIMARY_KEY_NAME = "fallback_rowid"
    FALLBACK_PRIMARY_KEY_DATATYPE = "INTEGER"
    ESCAPE_IDENTIFIER = "`"
    VARIABLE_SIZE_DATATYPES = set(["VARCHAR", "DECIMAL"])

    def __init__(self, access_db_cursor: pyodbc.Cursor, win32_db: typing.Any) -> None:
        self.logger = logging.getLogger(__name__)
        self.access_db_cursor = access_db_cursor
        self.win32_db = win32_db

    def generate_create_table_query(self, table_name: str) -> str:
        """Generate a MySQL query to create a Microsoft Access DB table in MySQL

        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: A MySQL query to create the table
        :rtype: str
        """
        missing_primary_keys = False
        primary_keys = self._get_primary_keys(table_name)
        fallback_primary_key_name = self._wrap_in_escape_identifier(TableCreator.FALLBACK_PRIMARY_KEY_NAME)
        if not primary_keys:
            missing_primary_keys = True
            primary_keys = [fallback_primary_key_name]
            
        column_parameters = self._get_column_parameters(table_name)

        # add auto-incrementing id if there's no primary key
        if missing_primary_keys:
            column_parameters.append(f"{fallback_primary_key_name} {TableCreator.FALLBACK_PRIMARY_KEY_DATATYPE} AUTO_INCREMENT")
        column_parameters.append(
            f"PRIMARY KEY ({', '.join(primary_keys)})"
        )
        column_parameters = ", ".join(column_parameters)
        self.logger.info(f"Genearted query for creating {table_name}")
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
                return [f"{self._wrap_in_escape_identifier(fld.Name)}" for fld in i.Fields]
            
    def _get_column_parameters(self, table_name: str) -> list[str]:
        """Generate all column parameters associated with a table

        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: The column parameters in a table
        :rtype: list[str]
        """
        column_parameters = []
        for row in self.access_db_cursor.columns(table=table_name):
            column_parameter = f"{self._wrap_in_escape_identifier(row.column_name)} {self._convert_to_mysql_datatype(row.type_name)}"
            if row.type_name in TableCreator.VARIABLE_SIZE_DATATYPES:
                column_parameter = self._update_variable_size_column_parameter(column_parameter, row, table_name)
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
            
    def _update_variable_size_column_parameter(self, column_parameter: str, row: typing.Any, table_name: str) -> str:
        """Update a column data type that accepts size parameters

        :param column_parameter: The current, incomplete column parameter. Variable
        parameters, such as size in VARCHAR, must be added
        :type column_parameter: str
        :param row: The current row in the Microsoft Access DB file
        :type row: typing.Any
        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: The completed column parameter
        :rtype: str column_parameter += f"({row.column_size})"
        """
        match row.type_name:
            case "VARCHAR":
                updated_with_size = f"{column_parameter}({row.column_size})"
                self.logger.info(f"{table_name}: updated {column_parameter} to {updated_with_size}")
                return updated_with_size
            case "DECIMAL":
                updated_with_size = f"{column_parameter}({row.column_size},{row.decimal_digits})"
                self.logger.info(f"{table_name}: updated {column_parameter} to {updated_with_size}")
                return updated_with_size
            case _:
                raise ValueError("Unrecognized variable-length data type")
            
    def _wrap_in_escape_identifier(self, column_name: str) -> str:
        """Wrap column name in MySQL escape identifier to avoid conflicts with MySQL keywords

        :param column_name: The column name
        :type column_name: str
        :return: The column name wrapped in escape identifiers
        :rtype: str
        """
        return f"{TableCreator.ESCAPE_IDENTIFIER}{column_name}{TableCreator.ESCAPE_IDENTIFIER}"