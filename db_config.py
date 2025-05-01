"""
Open/close database connections
"""
import configparser
import pathlib

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
    PORT_CONFIG_KEY

    def __init__(self, db_config_ini_file: pathlib.Path) -> None:
        self._validate_config_file(db_config_ini_file)
        config = configparser.ConfigParser()
        config.read(db_config_ini_file)
        self.user = config.get(Loader.CONFIG_SECTION, Loader.USER_CONFIG_KEY)
        self.hostname = config.get(Loader.CONFIG_SECTION, Loader.HOSTNAME_CONFIG_KEY)
        self.password = config.get(Loader.CONFIG_SECTION, Loader.PASSWORD_CONFIG_KEY)
        self.database = config.get(Loader.CONFIG_SECTION, Loader.DATABASE_CONFIG_KEY)
        self.port = config.get(Loader.CONFIG_SECTION, Loader.PORT_CONFIG_KEY)

    def _validate_config_file(self, db_config_ini_file: pathlib.Path) -> None:
        """Ensure config file exists and is an ini file

        :param db_config_ini_file: The path to the config file
        :type db_config_ini_file: pathlib.Path
        :raises FileNotFoundError: The path does not lead to an existing file
        :raises ValueError: The path does not lead to an ini file
        :raises ValueError: The file is missing the specified config section
        """
        if not os.path.exists(db_config_ini_file):
            raise FileNotFoundError(f"{db_config_ini_file} does not lead to a file")

        _, file_extension = os.path.splitext(db_config_ini_file)
        if file_extension != DBManager.CONFIG_FILE_EXTENSION:
            raise ValueError(f"{db_config_ini_file} does not lead to an ini file")
