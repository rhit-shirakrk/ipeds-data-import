"""
Manage Microsoft Access DB connection
"""

import os
import pathlib


import pyodbc


class AccessDBConnManager:
    DRIVER = "{Microsoft Access Driver (*.mdb, *.accdb)}"
    FILE_EXTENSION  = ".accdb"

    def __init__(self, access_db_file_path: pathlib.Path) -> None:
        self._validate_access_db(access_db_file_path)
        self.access_db_file_path = access_db_file_path

    def _validate_access_db(self, access_db_file_path: pathlib.Path) -> None:
        """Ensure Microsoft Access DB file exists and is an .accdb file

        :param access_db_file_path: The path to the Microsoft Access DB file
        :type access_db_file_path: pathlib.Path
        :raises FileNotFoundError: The path does not lead to an existing file
        :raises ValueError: The path does not lead to an accdb file
        """
        if not os.path.exists(access_db_file_path):
            raise FileNotFoundError(f"{access_db_file_path} does not lead to a file")

        _, file_extension = os.path.splitext(access_db_file_path)
        if file_extension != AccessDBConnManager.FILE_EXTENSION:
            raise ValueError(f"{access_db_file_path} does not lead to an {AccessDBConnManager.FILE_EXTENSION} file")

    def get_connection(self):
        """
        Return connection to Microsoft Access DB file
        """
        return pyodbc.connect(
            f"DRIVER={AccessDBConnManager.DRIVER};DBQ={self.access_db_file_path}"
        )
