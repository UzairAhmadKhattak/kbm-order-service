
from passlib.context import CryptContext
from .models import User,Role,UserInfo,Vehicle
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class UserCrud:
    @staticmethod
    def get_password_hash(password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        user = await db.execute(select(User).filter(User.username == username))
        return user.scalar_one_or_none()

    @staticmethod
    async def get_or_create_user_role(db: AsyncSession, role_name) -> Role | None:

        result = await db.execute(select(Role).filter(Role.name == role_name.value["name"]))
        role = result.scalar_one_or_none()
        if not role:
            role = Role(name=role_name.value["name"],
                        description=role_name.value["description"])
            db.add(role)
            await db.commit()
            await db.refresh(role)
        
        return role

    @staticmethod
    async def create_user(db: AsyncSession, is_commit=True, **kwargs) -> User:
        
        db_user = User(**kwargs)
        db.add(db_user)
        if is_commit is True:
            await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    async def create_more_user_info(db: AsyncSession, is_commit=True, **kwargs) -> None:

        more_user_info = UserInfo(**kwargs)
        db.add(more_user_info)
        if is_commit is True:
            await db.commit()


class VehicleCrud:
    @staticmethod
    async def create_vehicle(db: AsyncSession, is_commit=True, **kwargs) -> None:
        vehicle = Vehicle(**kwargs)
        db.add(vehicle)
        if is_commit is True:
            await db.commit()
