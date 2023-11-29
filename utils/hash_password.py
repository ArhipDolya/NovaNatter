import bcrypt


def hash_password(password: str) -> str :
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Convert the bytes to a string for storage in the database
    return hashed_password.decode('utf-8')