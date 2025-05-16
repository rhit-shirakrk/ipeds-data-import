import argparse
import logging
import pathlib
import sys

import win32com.client

import access_db
import data_importer
import db_config
import table_creator

if __name__ == "__main__":
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

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

    config_file_path = pathlib.Path(args.config_file)
    access_db_file_path = pathlib.Path(args.access_db_file)

    # used for fetching primary keys in tables
    db_engine = win32com.client.Dispatch("DAO.DBEngine.120")
    win32_db = db_engine.OpenDatabase(access_db_file_path)

    # used to connect to MySQL DB\
    mysql_manager = db_config.DBManager(config_file_path)
    mysql_table_creation_conn = mysql_manager.get_table_creation_connection()
    mysql_table_creation_conn_cursor = mysql_table_creation_conn.cursor()
    mysql_data_import_conn = mysql_manager.get_data_import_connection()

    # used for general-purpose tasks in Microsoft Access DB
    access_db_conn = access_db.AccessDBConnManager(access_db_file_path).get_connection()
    access_db_cursor = access_db_conn.cursor()

    # create MySQL tables
    tc = table_creator.TableCreator(access_db_cursor, mysql_table_creation_conn_cursor, win32_db)

    table_queries = []
    table_queries.append(f"USE {mysql_manager.database};")
    table_names = [table_info.table_name for table_info in access_db_cursor.tables(tableType="TABLE")]
    for table_name in table_names:
        table_query = tc.generate_create_table_query(table_name)
        table_queries.append(table_query)

    # store table generation query in file in case users need it later
    combined_table_query = "\n\n".join(table_queries) # added double newline for readability
    with open("ipeds_table_creation.sql", "x") as file:
        file.write(combined_table_query)

    # populate MySQL tables with data
    # di = data_importer.DataImporter(access_db_conn, mysql_data_import_conn)
    # for table_name in table_names:
    #     di.import_data(table_name)