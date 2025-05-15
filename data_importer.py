"""
Imports data from Micrsoft Access DB to MySQL
"""

import pandas as pd


class DataImporter:
    """
    Import data from specified Microsoft Access DB table
    """

    def __init__(self, mysql_conn) -> None:
        self.mysql_conn = mysql_conn

    def import_data(self, table_name: str) -> None:
        """Import data from Micrsoft Access DB table

        :param table_name: The name of the table whose data to import
        :type table_name: str
        """
        query = f"SELECT * FROM {table_name}"
        df = pd.read_csv(query, self.access_db_cursor)
        df.to_sql(table_name, self.mysql_conn, index=False)
