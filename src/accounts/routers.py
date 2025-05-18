from fastapi import APIRouter
from .schemas import UserCreate,UserRead
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..session import get_async_db
from .constants import UserConstants
from .cruds import (UserCrud,VehicleCrud)
from .schemas import (DelivererRegister,
                      UserSuccessResponse)
from fastapi import UploadFile,File
from typing import Optional,Annotated
from ..minio_setup import save_file_to_minio
from fastapi import Form
from pydantic import EmailStr
from datetime import date
from ..logger_config import setup_logger

logger = setup_logger(__name__)


router = APIRouter(prefix='/accounts',tags=['Accounts'])


@router.post('/customer_registration',response_model=UserSuccessResponse)
async def customer_registration(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    
    db_user = await UserCrud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail=UserConstants.USER_EXISTS.value)
    
    hashed_password = UserCrud.get_password_hash(user.password)

    role = await UserCrud.get_or_create_user_role(db,UserConstants.CUSTOMER_ROLE)

    await UserCrud.create_user(
                   db,
                   username=user.username,
                   email=user.email, 
                   full_name=user.full_name, 
                   hashed_password=hashed_password, 
                   is_active=True,
                   role_id=role.id)

    return UserSuccessResponse(message='Successfully Register the Customer')


@router.post('/deliverer_registration')
async def deliverer_registration(
    username: Annotated[str, Form(...)],
    email: Annotated[EmailStr, Form(...)],
    full_name: Annotated[str, Form(...)],
    password: Annotated[str, Form(..., min_length=8)],
    number_plate: Annotated[str, Form(...)],
    vehicle_type: Annotated[str, Form(...)],
    city: Annotated[str, Form(...)],
    address: Annotated[str, Form(...)],
    nic_number: Annotated[str, Form(...)],
    phone_number: Annotated[str, Form(...)],
    dob: Annotated[date, Form(...)],
    pic: Optional[UploadFile] = File(None),
    vehicle_doc: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_async_db),
):
    # Reconstruct DelivererRegister object
    deliverer = DelivererRegister(
        username=username,
        email=email,
        full_name=full_name,
        password=password,
        number_plate=number_plate,
        vehicle_type=vehicle_type,
        city=city,
        address=address,
        nic_number=nic_number,
        phone_number=phone_number,
        dob=dob,
    )

    db_user = await UserCrud.get_user_by_username(db, deliverer.username)
    if db_user:
        raise HTTPException(status_code=400, detail=UserConstants.USER_EXISTS.value)

    pic_url = await save_file_to_minio(pic,f"profile_pics/{deliverer.username}_{pic.filename}")
    vehicle_doc_url = await save_file_to_minio(vehicle_doc,f"vehicle_docs/{deliverer.username}_{pic.filename}")

    user = deliverer.user.dict()
    vehicle = deliverer.vehicle.dict()
    more_user_info = deliverer.more_user_info.dict()

    user['hashed_password'] = UserCrud.get_password_hash(user['password'])
    user.pop('password')
    try:
        user = await UserCrud.create_user(db, is_active=False, **user)

        await UserCrud.create_more_user_info(db, False,
                                             **more_user_info,
                                             user_id=user.id,
                                             pic_url=pic_url)

        await VehicleCrud.create_vehicle(db, False,
                                         **vehicle,
                                         user_id=user.id,
                                         vehicle_doc_url=vehicle_doc_url)
        await db.commit()
    except Exception as e:
        logger.error(f'Unable to create register deliverer:{e}')
        await db.rollback()
        raise HTTPException(status_code=400, detail='Something went wrong')

    return UserSuccessResponse(message='Successfully Register the deliverer')




