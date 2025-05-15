"""
Imports data from Micrsoft Access DB to MySQL
"""

import logging

import pandas as pd


class DataImporter:
    """
    Import data from specified Microsoft Access DB table
    """

    def __init__(self, access_db_conn, mysql_conn) -> None:
        self.logger = logging.getLogger(__name__)
        self.access_db_conn = access_db_conn
        self.mysql_conn = mysql_conn

    def import_data(self, table_name: str) -> None:
        """Import data from Micrsoft Access DB table

        :param table_name: The name of the table whose data to import
        :type table_name: str
        """
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, self.access_db_conn)
        df.to_sql(table_name, self.mysql_conn, index=False)
        self.logger.info(f"Successfully imported data to {table_name}")
