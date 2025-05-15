"""
Manage Microsoft Access DB connection
"""

import pathlib

import pyodbc


class AccessDBConnManager:
    DRIVER = "{Microsoft Access Driver (*.mdb, *.accdb)}"

    def __init__(self, file_path: pathlib.Path) -> None:
        self.file_path = file_path

    def get_connection(self):
        """
        Return connection to Microsoft Access DB file
        """
        return pyodbc.connect(
            f"DRIVER={AccessDBConnManager.DRIVER};DBQ={self.file_path}"
        )
