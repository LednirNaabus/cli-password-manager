import os
import sqlite3 as db
from dotenv import load_dotenv

load_dotenv()

db_name = os.environ["DB_NAME"]
db_dir = 'databases'

def make_dir():
    try:
        os.makedirs(db_dir)
    except OSError as ose:
        if os.path.isdir(db_dir):
            print(f"db.py Error: {ose}")

def createDB():
    conn = None
    try:
        if not os.path.exists(db_dir):
            make_dir()
            conn = db.connect(os.path.join(db_dir, db_name))
            print(f"Database {db_name} successfully created!")
            print(f"Connection at: {conn}")
        elif os.path.exists(db_dir):
            print(f"Error! Database {db_dir}/{db_name} already exists!")
            print("Exiting program...")
            pass
    except db.Error as e:
        print(e)

    return conn

createDB()
