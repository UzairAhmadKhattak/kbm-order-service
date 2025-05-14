
from passlib.context import CryptContext
from .models import User,Role
from sqlalchemy.orm import Session


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


class UserCrud:

    def get_user_by_username(self,db:Session, username:str) -> User:
        return db.query(User).filter(User.username == username).first()
    

    def get_or_create_user_role(self,db:Session,role_name) -> Role:

        role = db.query(Role).filter(Role.name==role_name.value["name"])
        if not role:
            role = Role(name=role_name.value["name"],
                        description=role_name.value["description"])
            db.add(role)
            db.commit()
            db.refresh(role)
        else:
            role = role.first()
        
        return role
    
    def create_customer(self,db:Session,**kwargs) -> User:
        
        db_user = User(**kwargs)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user