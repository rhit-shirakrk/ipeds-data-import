"""
Open/close database connections
"""

import configparser
import os
import pathlib

import mysql.connector
import sqlalchemy


class DBManager:
    """Load a database config file to upload data to a database

    :param db_config_ini_file: The path to the ini config file
    :type db_config_ini_file: pathlib.Path
    """

    CONFIG_FILE_EXTENSION = ".ini"
    CONFIG_SECTION = "ipeds_db"
    USER_CONFIG_KEY = "user"
    PASSWORD_CONFIG_KEY = "password"
    HOSTNAME_CONFIG_KEY = "hostname"
    DATABASE_CONFIG_KEY = "database"
    PORT_CONFIG_KEY = "port"

    def __init__(self, db_config_ini_file: pathlib.Path) -> None:
        self._validate_config_file(db_config_ini_file)
        config = configparser.ConfigParser()
        config.read(db_config_ini_file)
        self.user = config.get(DBManager.CONFIG_SECTION, DBManager.USER_CONFIG_KEY)
        self.hostname = config.get(
            DBManager.CONFIG_SECTION, DBManager.HOSTNAME_CONFIG_KEY
        )
        self.password = config.get(
            DBManager.CONFIG_SECTION, DBManager.PASSWORD_CONFIG_KEY
        )
        self.database = config.get(
            DBManager.CONFIG_SECTION, DBManager.DATABASE_CONFIG_KEY
        )
        self.port = config.get(DBManager.CONFIG_SECTION, DBManager.PORT_CONFIG_KEY)

    def _validate_config_file(self, db_config_ini_file: pathlib.Path) -> None:
        """Ensure config file exists and is an ini file

        :param db_config_ini_file: The path to the config file
        :type db_config_ini_file: pathlib.Path
        :raises FileNotFoundError: The path does not lead to an existing file
        :raises ValueError: The path does not lead to an ini file
        """
        if not os.path.exists(db_config_ini_file):
            raise FileNotFoundError(f"{db_config_ini_file} does not lead to a file")

        _, file_extension = os.path.splitext(db_config_ini_file)
        if file_extension != DBManager.CONFIG_FILE_EXTENSION:
            raise ValueError(f"{db_config_ini_file} does not lead to an ini file")

    def get_data_import_connection(self) -> sqlalchemy.Engine:
        """Creates connection to database meant for importing data

        :return: Connection to database
        :rtype: sqlalchemy.Engine
        """
        return sqlalchemy.create_engine(
            f"mysql+mysqlconnector://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.database}"
        )

    def get_table_creation_connection(
        self,
    ) -> (
        mysql.connector.pooling.PooledMySQLConnection
        | mysql.connector.abstracts.MySQLConnectionAbstract
    ):
        """Creates connection to database meant for creating tables

        :return: Connection to database
        :rtype: mysql.PooledMySQLConnection | mysql.MySQLConnectionAbstract
        """
        return mysql.connector.connect(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.hostname,
            port=self.port,
        )

