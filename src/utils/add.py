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

def check_entry(entry_name, email, username, is_OTP):
    database = DatabaseConfig.DatabaseConfig(db_directory, db_name)
    db_conn = database.connect_db()
    print(db_conn)
    db_curr = db_conn.cursor()
    is_OTP = 1 # default
    q = f'SELECT * FROM entries WHERE entry_name="{entry_name}" AND email="{email}" AND username="{username}" AND is_OTP="{is_OTP}"'
    db_curr.execute(q)
    results = db_curr.fetchall()

    if len(results) != 0:
        return True
    db_curr.close()
    db_conn.close()
    return False

def add_entry(master_pass, ds, entry_name, email, username, is_OTP):
    if check_entry(entry_name, email, username, is_OTP):
        print(f"Entry already exists")
        return

    passwd = getpass("Password: ")

    mk = compute_masterkey(master_pass, ds)
    encrypted = aesu.encrypt(key=mk, source=passwd, keyType="bytes")

    database = DatabaseConfig.DatabaseConfig(db_directory, db_name)
    with database.connect_db() as conn:
        db_curr = conn.cursor()
        q = "INSERT INTO entries (entry_name, email, username, password, is_OTP) VALUES (?, ?, ?, ?, ?)"
        val = (entry_name, email, username, is_OTP, encrypted)
        db_curr.execute(q, val)
        print("Added entry.")
