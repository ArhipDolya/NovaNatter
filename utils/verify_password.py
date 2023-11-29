from passlib.context import CryptContext


def verify_user_password(plain_password: str, hashed_password: str) -> bool:
    """
        Verify a plain password against a hashed password.

        Returns:
        - bool: True if the passwords match, False otherwise.
    """

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    return pwd_context.verify(plain_password, hashed_password)