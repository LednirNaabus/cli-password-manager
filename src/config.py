# This is the config file
# This is the first script that runs during first-time installation
import sys
import getpass
import hashlib
import string
import random
import logging
import os

from dotenv import load_dotenv
from utils.db import DatabaseConfig

load_dotenv()

# You can change the values in your .env
db_name = os.environ["DB_NAME"]
db_directory = os.environ["DB_DIRECTORY"]

def gen_device_secret(length: int = 10) -> str:
    """
    Generates device secret of the specified length.

    Args:
        length (int, optional): The length of the desired string. Default is 10.

    Returns:
        str: A random string of the specified length.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def config():
    database = DatabaseConfig(db_directory, db_name)
    print("Creating new config file...\n\n", flush=True)
    try:
        database.create_db()
        # note: using context manager autocommits apparently
        # so there's no need to use .commit()
        with database.connect_db() as conn:
            db_cur = conn.cursor()

            query = "CREATE TABLE master_table (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
            res = db_cur.execute(query)
            print("Table 'master_table' successfully created.", flush=True)

            query = "CREATE TABLE entries (entry_name TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL, is_OTP BOOLEAN NOT NULL)"
            res = db_cur.execute(query)
            print("Table 'entries' successfully created.", flush=True)

            master_pass = ""
            print("Note: The master password is the one you will need to remember to access your other passwords.")
            
            while 1:
                master_pass = getpass.getpass("Enter your master password:")
                if master_pass == getpass.getpass("Re-type your master password:") and master_pass != "":
                    break
                print("Please try again.")

            # hashing the master password
            hashed_mp = hashlib.sha256(master_pass.encode()).hexdigest()
            print("Hash generated for master password.")

            # Generate device secret
            dev_sec = gen_device_secret()
            print("Successfully generated device secret.")

            query = "INSERT INTO master_table (masterkey_hash, device_secret) values (?,?)"
            values = (hashed_mp, dev_sec)
            db_cur.execute(query, values)

            print("Successfully inserted master password and device secret to 'master_table'!")
            print("Configuration done.\n")
            db_cur.close()
    except Exception as e:
        print(f"config.py error: {e}")
        sys.exit()

def main():
    config()

if __name__ == "__main__":
    main()
