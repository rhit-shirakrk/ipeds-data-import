"""
Creates MySQL tables from Microsoft Access DB tables
"""

import pandas as pd
import win32com.client


class MySQLTable:
    """Representation of a MySQL table resulting from a Microsoft Access DB table

    :param table_name: The name of the table in MySQL
    :type table_name: str
    :param column_name_to_datatype: A mapping between each column and its expected
    datatype
    :type column_name_to_datatype: dict[str, Any]
    """

    def __init__(
        self, table_name: str, column_name_to_datatype: dict[str, Any]
    ) -> None:
        self.table_name = table_name
        self.column_name_to_datatype = column_name_to_datatype

    def generate_empty_table(self) -> pd.DataFrame:
        """Generate table from specified table name and column datatype mappings

        :return: A Python representation of the table
        :rtype: pd.DataFrame
        """


class TableCreator:
    """
    Get table schematics from a Microsoft Access DB file, then create a
    representation of that table in Python
    """

    def __init__(self, access_db_cursor, mysql_cursor, win32_db) -> None:
        self.access_db_cursor = access_db_cursor
        self.mysql_cursor = mysql_cursor
        self.win32_db = win32_db

    def create_table(self, table_name: str) -> None:
        """Create a table using the given table name

        :param table_name: The name of the table to create in Python
        :type table_name: str
        """
        self.mysql_cursor.execute(self._generate_create_table_query(table_name))

    def _generate_create_table_query(self, table_name: str) -> str:
        """Generate a CREATE TABLE MySQL query based on the column names,
        types, and schematics of the table

        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: A query string to create the schematics of an Access DB table
        in MySQL
        :rtype: str
        """
        table_parameters = self._generate_table_parameters(table_name)
        table_parameters.append(self._generate_primary_keys_as_table_parameter())

        return f"CREATE TABLE {table_name}({table_parameters})"

    def _generate_table_parameters(self, table_name: str) -> list[str]:
        """Generate a list of table parameters mapping columns to their data type

        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: A list of columns and their data types
        :rtype: list[str]
        """
        return [
            f"{row.column_name} {row.type_name}"
            for row in access_db_cursor.columns(table=table_name)
        ]

    def _generate_primary_keys_as_table_parameter(self, table_name: str) -> str:
        """Generate a string that sets primary keys on a MySQL table

        :param table_name: The name of the table to create in Python
        :type table_name: str
        :return: Primary key table constraints
        :rtype: str
        """
        return f"PRIMARY KEY ({', '.join(self._get_primary_keys(table_name))})"

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
