# Outline
- Command Line Interface
- Get master password
    - Validate master password
    - If validated: show saved passwords, otherwise exit
- Copy passwords to clipboards
- Can add, edit, view, and delete entries
- This CLI program can be installed using `pip` or through `git` (**Note:** Create an installation script in bash)
- Passwords/entries is saved on a local SQL database

## Implementation

### Configuration
- A **master password** must be created after first installing. Save the master password (hashed) in a local file.
- `DEVICE_SECRET` will be a randomly generated string, also stored in a file (used as a salt)
- **Master password** and `DEVICE_SECRET` is combined and passed into a hashing function to create a valid key for AES-256. This is the `master key`.
- `master key` is used to decrypt and encrypt passwords and entries.

### Adding New Entry
- Ask for **master password** first
- Validate the **master password** by hashing and checking with existing hash
- Input fields for adding entry:
    - name/entry_name
    - email
    - username
    - password
    - `is_OTP`
    - `category`
- Encrypt the email, username, password with `master key` and then save the fields into the database.

### Updating entry
- Working on it...

### View entry
- Input field to search for (entry_name, email, username)
- Display all the entries that match the search. Passwd is hidden by default.
- Using `-p`:
    - Ask for **master password**
    - Validate
    - Decrypt the passwd and copy to clipboard

---

### Concepts
- Encrypted fields: email, username, password
- Plain: site/entry name, `is_OTP` (boolean; checks whether or not is in Google Authenticator or in Authy), `category`: type of entry (email/wifi/banking etc.)

## Reference
- This project is based on an existing project by TechRaj (https://youtu.be/KQjf9get6PE?si=x5gHGgrAGlamgony)
