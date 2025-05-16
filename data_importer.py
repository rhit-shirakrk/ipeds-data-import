"""
Imports data from Micrsoft Access DB to MySQL
"""

import logging
import traceback

import pandas as pd


class DataImporter:
    """
    Import data from specified Microsoft Access DB table
    """

    def __init__(self, access_db_manager, mysql_manager) -> None:
        self.logger = logging.getLogger(__name__)
        self.access_db_manager = access_db_manager
        self.mysql_manager = mysql_manager

    def import_data(self, table_name: str) -> None:
        """Import data from Micrsoft Access DB table

        :param table_name: The name of the table whose data to import
        :type table_name: str
        """
        query = f"SELECT * FROM {table_name}" # normally bad practice, but we want to fetch all columns including new ones that weren't in previous years

        try:
            access_db_conn = self.access_db_manager.get_connection()
            df = pd.read_sql(query, access_db_conn)
            access_db_conn.close()

            mysql_conn = self.mysql_manager.get_data_import_connection()
            df.to_sql(table_name, mysql_conn, if_exists="append", index=False)
            mysql_conn.dispose()

            print(f"Successfully imported data to {table_name}")
            self.logger.info(f"Successfully imported data to {table_name}")
        except Exception as e:
            self.logger.error(traceback.format_exc())