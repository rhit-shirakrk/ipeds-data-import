import argparse
import pathlib
import sys

import win32com.client

import access_db
import data_importer
import db_config
import table_creator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", type=str)
    parser.add_argument("-a", "--access-db-file", type=str)
    args = parser.parse_args()

    if not args.config_file:
        print("Path to config file required")
        sys.exit(1)

    if not args.access_db_file:
        print("Path to Microsoft Access DB file required")
        sys.exit(1)

    # used for fetching primary keys in tables
    db_engine = win32com.client.Dispatch("DAO.DBEngine.120")
    win32_db = db_engine.OpenDatabase(MDB)

    # used to connect to MySQL DB
    mysql_conn = db_config.DBManager(args.config_file).get_db_connection()
    mysql_cursor = mysql_conn.cursor()

    # used for general-purpose tasks in Microsoft Access DB
    access_db_conn = access_db.AccessDBConnManager(
        pathlib.Path(args.access_db_file)
    ).get_connection()
    access_db_cursor = access_db_conn.cursor()

    # create MySQL tables
    tc = table_creator.TableCreator(access_db_cursor, mysql_cursor, win32_db)
    for table_info in access_db_cursor.tables(tableType="TABLE"):
        tc.create_table(table_info.table_name)

    # populate MySQL tables with data
    di = data_importer.DataImporter(mysql_conn)
    for table_info in access_db_cursor.tables(tableType="TABLE"):
        di.import_data(table_info.table_name)
