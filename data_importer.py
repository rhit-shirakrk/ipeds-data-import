"""
Imports data from Micrsoft Access DB to MySQL
"""

import logging
import traceback

import pandas as pd

import access_db
import db_config


class DataImporter:
    """Import data from specified Microsoft Access DB table

    :param access_db_manager: Access point to create a connection to a Microsoft Access DB file
    :type access_db_manager: access_db.AccessDBConnManager
    :param mysql_manager: Access point to create a connection to a MySQL database
    :type mysql_manager: db_config.DBManager
    """
    ROWS_PER_CHUNK = 200000

    def __init__(self, access_db_manager: access_db.AccessDBConnManager, mysql_manager: db_config.DBManager) -> None:
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
            for chunk in pd.read_sql(query, access_db_conn, chunksize=DataImporter.ROWS_PER_CHUNK):
                mysql_conn = self.mysql_manager.get_data_import_connection()
                chunk.to_sql(table_name, mysql_conn, if_exists="append", index=False)
                mysql_conn.dispose()

                self.logger.info(f"Imported {len(chunk.index)} rows from {table_name}")
            access_db_conn.close()

            success_message = f"Successfully imported data from {table_name}"
            print(success_message)
            self.logger.info(success_message)
        except Exception as e:
            error_message = f"Failed to import data from {table_name}"
            print(error_message)
            self.logger.info(error_message)
            self.logger.error(traceback.format_exc())