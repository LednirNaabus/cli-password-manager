import utils.DatabaseConfig as DatabaseConfig
import utils.aesutil as aesu
from getpass import getpass

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import base64, os
from dotenv import load_dotenv

load_dotenv()

db_name = os.environ["DB_NAME"]
db_directory = os.environ["DB_DIRECTORY"]

def compute_masterkey(master_passwd, ds):
    passwd = master_passwd.encode()
    salt = ds.encode()
    key = PBKDF2(passwd, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key

def check_entry(entry_name, email, username, password, is_OTP: bool, category):
    database = DatabaseConfig.DatabaseConfig(db_directory, db_name)
    # db_conn = database.create_db()
    db_conn = database.connect_db()
    print(db_conn)
    # cursor = db_conn.cursor()
    # if check_entry(entry_name, email, username, password, is_OTP, category):
        # print("Entry already exists!")
        # return

    # password = getpass("Password: ")

    # master_k = compute_masterkey()
