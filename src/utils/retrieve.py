import utils.DatabaseConfig as Db
import utils.aesutil as aesu
import pyperclip

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import base64, os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

db_name = os.environ["DB_NAME"]
db_directory = os.environ["DB_DIRECTORY"]

def compute_masterkey(master_passwd, ds):
    passwd = master_passwd.encode()
    salt = ds.encode()
    key = PBKDF2(passwd, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key

def get_entries(master_passwd, ds, search_query, decrypt_pass=False):
    database = Db.DatabaseConfig(db_directory, db_name)
    with database.connect_db() as conn:
        db_cur = conn.cursor()
        q = ""
        if len(search_query)==0:
            q = "SELECT * FROM entries"
        else:
            q = "SELECT * FROM entries WHERE "
            for i in search_query:
                q += f'{i} = "{search_query[i]}" AND '
            q = q[:-5]

        db_cur.execute(q)
        res = db_cur.fetchall()

        if len(res) == 0:
            print("No results found.")
            return

        if(decrypt_pass and len(res) > 1) or (not decrypt_pass):
            if decrypt_pass:
                print("More than one result found")
            table = Table(title="Results")
            table.add_column("Name")
            table.add_column("Email")
            table.add_column("Username")
            table.add_column("is_OTP")
            table.add_column("Password")

            for i in res:
                table.add_row(i[0], i[1], i[2], i[3], "{hidden}")
            console = Console()
            console.print(table)
            return
            
        if decrypt_pass and len(res) == 1:
            master_key = compute_masterkey(master_passwd, ds)
            decrypted = aesu.decrypt(key=master_key, source=res[0][4], keyType="bytes")
            print("Password copied to clipboard.")
            pyperclip.copy(decrypted.decode())
