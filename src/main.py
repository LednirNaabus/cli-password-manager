import argparse
import hashlib
from getpass import getpass
import os

import utils.add as add
import utils.retrieve as ret
from utils.DatabaseConfig import DatabaseConfig

from dotenv import load_dotenv

load_dotenv()

db_name = os.environ["DB_NAME"]
db_directory = os.environ["DB_DIRECTORY"]

parser = argparse.ArgumentParser(description='Description')
parser.add_argument('option', help='(a)dd')
parser.add_argument('-n', '--name', help='Entry name (site, etc.)')
parser.add_argument('-t', '--type', help='Category/Type of entry (email, wifi password, credit card credentials, etc.). This argument can also act as a short note or description of your entry. Remember to enclose them with quotation marks.')
parser.add_argument('-e', '--email', help='Email')
parser.add_argument('-u', '--username', help='Username')
parser.add_argument('-o', '--otp', help='Has OTP enabled (1 or 0)')
parser.add_argument('-c', '--copy', action='store_true', help='Copy to clipboard selected entry.')
args = parser.parse_args()

def auth():
    mp = getpass("Enter your master password: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    database = DatabaseConfig(db_directory, db_name)
    with database.connect_db() as conn:
        db_cur = conn.cursor()
        q = "SELECT * FROM master_table"
        db_cur.execute(q)
        res = db_cur.fetchall()[0]
        if hashed_mp != res[0]:
            print("wrong password.")
            return None
        db_cur.close()
        return [mp, res[1]]

def main():
    if args.option in ["add", "a"]:
        if args.name == None or args.type == None or args.email == None or args.username == None or args.otp == None:
            if args.name == None:
                print("Entry name (-n) required.")
            if args.type == None:
                print("Category/Type (-t) required.")
            if args.email == None:
                print("Email (-e) required.")
            if args.username == None:
                print("Username (-u) required.")
            if args.otp == None:
                print("OTP enabled (-o) required.")
            return
        res = auth()
        if res is not None:
            add.add_entry(res[0], res[1], args.name, args.type, args.email, args.username, args.otp)

    if args.option in ["extract", "e"]:
        res = auth()
        search = {}

        if args.name is not None:
            search["entry_name"] = args.name
        if args.type is not None:
            search["type"] = args.type
        if args.email is not None:
            search["email"] = args.email
        if args.username is not None:
            search["username"] = args.username
        if args.otp is not None:
            search["is_OTP"] = args.otp

        if res is not None:
            ret.get_entries(res[0], res[1], search, decrypt_pass = args.copy)

main()
