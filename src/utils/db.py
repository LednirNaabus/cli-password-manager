import os, sys
import sqlite3 as db
import logging
from dotenv import load_dotenv

load_dotenv()

# You can change the values in your .env
db_name = os.environ["DB_NAME"]
db_directory = os.environ["DB_DIRECTORY"]

class DatabaseConfig:
    def __init__(self, database_directory, database_name):
        self.database_directory = database_directory
        self.database_name = database_name

        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)

# Create directory for database
# def make_dir():
    # try:
        # os.makedirs(db_directory)
    # except OSError as ose:
        # if os.path.isdir(db_directory):
            # print(f"db.py Error: {ose}")

# create database
# def create_db():
    # conn = None
    # try:
        # if not os.path.exists(db_directory):
            # print(f"Directory: '{db_directory}' does not exist. Creating directory...")
            # make_dir()
            # print(f"'{db_directory}' successfully created!")
            # conn = db.connect(os.path.join(db_directory, db_name))
            # print(f"Database {db_name} successfully created!")
            # print(f"Database file located at: {os.path.abspath(db_name)}")
            # print(f"Connection at: {conn}")
        # elif os.path.exists(db_directory):
            # print(f"Error! Database '{db_directory}/{db_name}' already exists!")
            # print("Exiting program...\n")
            # sys.exit()
    # except db.Error as e:
        # print(e)

    # return conn
