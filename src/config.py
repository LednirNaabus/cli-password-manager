# This is the config file
# This is the first script that runs during first-time installation
from os.path import isfile
import sys
import getpass
import hashlib
import string
import random
import os

# other modules, packages, etc
import utils
from utils.DatabaseConfig import DatabaseConfig

from dotenv import load_dotenv

load_dotenv()

# You can change the values in your .env
db_name = os.environ["DB_NAME"]
db_directory = os.environ["DB_DIRECTORY"]

def check_config_log(file: str) -> bool:
    """
    Checks 'config.log' inside the directory.
    Args:
        file (str, required): String of the file name. Default: 'config.log'.
    Returns:
        bool: Whether or not the log file exists. Returns 'True' if found, 'False' if not found.
    """
    print("Checking if config file exists...")
    if os.path.isfile(file):
        print(f"Existing config file ('config.log') found! Delete existing config file first before creating a new config file. (Hint: try using 'config delete')\n")
        return True
    else:
        return False

def gen_device_secret(length: int = 10) -> str:
    """
    Generates device secret of the specified length.

    Args:
        length (int, optional): The length of the desired string. Default is 10.

    Returns:
        str: A random string of the specified length.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def config(config_logger):
    # if 'config.log' not found, create new one
    if not check_config_log('config.log'):
        config_logger = utils.log_util.setup_logger('config_log', 'config.log')
    else:
        return
    print("Creating new config file...\n\n", flush=True)
    try:
        # database = utils.DatabaseConfig.DatabaseConfig(db_directory, db_name)
        database = DatabaseConfig(db_directory, db_name)
        database.create_db()
        # note: (sqlite3) using context manager autocommits apparently
        # so there's no need to use .commit()
        with database.connect_db() as conn:
            db_cur = conn.cursor()

            query = "CREATE TABLE master_table (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
            res = db_cur.execute(query)
            config_logger.info("Table 'master_table' successfully created.")

            query = "CREATE TABLE entries (entry_name TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL, is_OTP BOOLEAN NOT NULL)"
            res = db_cur.execute(query)
            config_logger.info("Table 'entries' successfully created.")

            master_pass = ""
            print("Note: The master password is the one you will need to remember to access your other passwords.")
            
            while 1:
                master_pass = getpass.getpass("Enter your master password:")
                if master_pass == getpass.getpass("Re-type your master password:") and master_pass != "":
                    break
                print("Please try again.")

            # hashing the master password
            hashed_mp = hashlib.sha256(master_pass.encode()).hexdigest()
            config_logger.info("Hash generated for master password.")

            # Generate device secret
            dev_sec = gen_device_secret()
            config_logger.info("Successfully generated device secret.")

            query = "INSERT INTO master_table (masterkey_hash, device_secret) values (?,?)"
            values = (hashed_mp, dev_sec)
            db_cur.execute(query, values)

            config_logger.info("Successfully inserted master password and device secret to 'master_table'!")
            config_logger.info("Configuration done. Closing connection...\n")
            db_cur.close()
    except Exception as e:
        print(f"config.py error: {e}")
        sys.exit()

def delete_config(config_logger):
    """
    Will delete the config files except for 'config.log' since 'config.log' also stores the log for file deletion.
    Args:
        config_logger (required): Handler for the config file.
    """

    # will store delete logs to the config.log file
    config_logger = utils.log_util.setup_logger('config_log', 'config.log')
    config_logger.warning("You are about to delete existing config files! ('pw.db')")

    while 1:
        ans = input("Are you sure? y/N: ")
        if ans.upper() == "Y":
            break
        # default answer: N
        if ans.upper() == "N" or ans == "":
            sys.exit(0)
        else:
            continue

    if not os.path.exists('databases/pw.db'):
        print("No database found.")
    else:
        config_logger.info("Deleting config files...\n")
        try:
            config_logger.info(f"Database found: {os.path.abspath('pw.db')}.")
            config_logger.info("Deleting database config files...")
            os.remove('databases/pw.db')
            os.removedirs('databases')
            config_logger.info("Config files deleted.")
        except Exception as e:
            config_logger.error(f"{e}")

def main():
    cl = None
    if len(sys.argv) != 2:
        print("Usage: python config.py [options: new, delete]")
        sys.exit(0)

    if sys.argv[1] == "new":
        config(cl)
    elif sys.argv[1] == "delete":
        delete_config(cl)
    else:
        print("Usage: python config.py [options: new, delete]")

if __name__ == "__main__":
    main()
