# Outline

- Command Line Interface
- Get master password
    - Validate master password
    - If validated: show saved passwords, otherwise exit
- Copy passwords to clipboards
- Can add, edit, view, and delete entries
- The CLI can be installed using pip (**Note:** Create an installation script in bash)
- Passwords/entries is saved on a local SQL database

## Implementation

### Configuration

- A **master password** must be created after first installing. Save the master password (hashed) in a local file.
- `DEVICE_SECRET` will be a randomly generated string, also stored in a file (used as a salt)
