# When dealing with user's passwords, we cannot store plaintext passwords in database
# so, we need certain functions that hash (no way of return to plaintext) those passwords
# and, later when user tries to login (or do something) with their plaintext password, then it matches the hashed password
# (hashed data cannot be reversed to previous form, making it incredibly secure, as the code that hashed it, is capable to validate it (dunno how))
# its a core utility on which the architecture (security part) depends on, so we should store it in core/ folder

# Imports
import bcrypt

# We use bcrypt, the industry standard hashing algorithm
# this returns an object consisting of several methods 
# (which means, when created an object out of it, it carries all the tools to deal with the data in its lifecycle)
# (maybe that's why it have naming pws_context => password-context, carrying all capabilites for the password within object)
# # bcrypt pours "salt" in the "raw" password :)


# Defined

def get_password_hash(password: str) -> str:
    """Scrambles a raw password into a secure hash"""
    
    password_in_bytes = password.encode('utf-8')                # cryptography requires bytes, not strings!
    salt = bcrypt.gensalt()                                     # generates a random salt
    hashed_password = bcrypt.hashpw(password_in_bytes, salt)    # hashes the password, while combining the salt

    return hashed_password.decode('utf-8')                      # gets stored in database (we can store "encoded" passwords, but our user model have String type_ in models/user.py file)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain password matches the scrambled hash in the database"""
   
    password_in_bytes = plain_password.encode('utf-8')
    hashed_password_in_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_in_bytes, hashed_password_in_bytes)
