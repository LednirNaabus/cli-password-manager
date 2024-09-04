import os, sys
import sqlite3 as db
from .log_util import setup_logger

db_logger = setup_logger('db_log', 'db.log')

"""
Class for a database config (sqlite3). A logger is instantiated with it and will also create a new 'db.log' file in the root directory.
"""
class DatabaseConfig:
    def __init__(self, database_directory: str, database_name: str):
        self.database_directory = database_directory
        self.database_name = database_name
        self.logger = db_logger

    def dir_exists(self) -> bool:
        self.logger.info(f"Checking if directory '{self.database_directory}' exists.")
        if os.path.exists(self.database_directory):
            self.logger.info(f"Directory '{self.database_directory}' already exists! Exiting program...")
            return True
        else:
            self.logger.info(f"Directory does not exist. Creating '{self.database_directory}'...")
            return False

    def make_dir(self):
        self.logger.info(f"Directory '{self.database_directory}' successfully created!")
        return os.makedirs(self.database_directory)

    def create_db(self):
        """
        Creates a new database file only. If a database file already exists, terminates the program.
        """
        db_file = None
        try:
            if not self.dir_exists():
                self.make_dir()
                db_path = os.path.join(self.database_directory, self.database_name)
                db_file = db.connect(db_path)
                self.logger.info(f"Database '{self.database_name}' successfully created!")
                self.logger.info(f"Database '{self.database_name}' file located at: {os.path.abspath(db_path)}.")
            else:
                self.logger.error(f"Database '{self.database_directory}/{self.database_name}' already exists! Exiting program...")
                sys.exit()
        except db.Error as e:
            self.logger.error(f"{e}")
        finally:
            if db_file:
                db_file.close()
        return db_file

    def connect_db(self):
        filename = os.path.join(self.database_directory, self.database_name)
        db_conn = db.connect(filename)
        self.logger.info(f"Database connection: '{db_conn}'")
        return db_conn
