import argparse
import db_config
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", type=str)
    args = parser.parse_args()

    if not args.config_file:
        print("Path to config file required")
        sys.exit(1)

    c = db_config.DBManager(args.config_file)
