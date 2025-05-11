from fastapi import APIRouter
from .schemas import UserCreate,UserRead
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ..session import get_db
from .models import User,Role
from .constants import UserConstants
from passlib.context import CryptContext

router = APIRouter(prefix='/accounts')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post('/customer_registration',response_model=UserRead)
async def customer_registration(user: UserCreate, db:Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail= UserConstants.USER_EXISTS.value)
    
    hashed_password = get_password_hash(user.password)
    role = db.query(Role).filter(Role.name==UserConstants.CUSTOMER_ROLE.value["name"])
    if not role:
        role = Role(name=UserConstants.CUSTOMER_ROLE.value["name"],
                     description=UserConstants.CUSTOMER_ROLE.value["description"])
        db.add(role)
        db.commit()
        db.refresh(role)
    else:
        role = role.first()

    db_user = User(username=user.username, 
                   email=user.email, 
                   full_name=user.full_name, 
                   hashed_password=hashed_password, 
                   is_active=True,role_id=role.id)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

    
