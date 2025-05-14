from fastapi import APIRouter
from .schemas import UserCreate,UserRead
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ..session import get_db
from .models import User,Role
from .constants import UserConstants
from .cruds import get_password_hash,UserCrud

user_crud = UserCrud()

router = APIRouter(prefix='/accounts',tags=['Accounts'])


@router.post('/customer_registration',response_model=UserRead)
async def customer_registration(user: UserCreate, db:Session = Depends(get_db)):
    
    db_user = user_crud.get_user_by_username(db,user.username)
    if db_user:
        raise HTTPException(status_code=400, detail= UserConstants.USER_EXISTS.value)
    
    hashed_password = get_password_hash(user.password)

    role = user_crud.get_or_create_user_role(db,UserConstants.CUSTOMER_ROLE)

    db_user = user_crud.create_customer(username=user.username, 
                   email=user.email, 
                   full_name=user.full_name, 
                   hashed_password=hashed_password, 
                   is_active=True,role_id=role.id)
    return db_user

    
