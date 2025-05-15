import argparse
import pathlib
import sys

import access_db
import db_config

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

    db_conn = db_config.DBManager(args.config_file)

    access_db_file_path = pathlib.Path(args.access_db_file)

    access_db_conn_manager = access_db.AccessDBConnManager(access_db_file_path)
    access_db_conn = access_db_conn_manager.get_connection()
