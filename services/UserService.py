from sqlalchemy.orm import Session

from models.model import User
from schemas.UserSchema import UserSchema, UserLoginSchema

from utils.hash_password import hash_user_password
from utils.verify_password import verify_user_password

from auth.jwt_handler import sign_JWT


class UserService:

    @staticmethod
    def create_user(db: Session, user: UserSchema):
        hashed_password = hash_user_password(user.password1)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def login_user(db: Session, user: UserLoginSchema):
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user and verify_user_password(user.password1, db_user.hashed_password):
            token = sign_JWT(db_user.id)
            return token
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")