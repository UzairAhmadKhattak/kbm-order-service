from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey,
                        Date,
                        Boolean,
                        Text)
from sqlalchemy.orm import relationship
from src.base_model import Base

metadata = Base.metadata

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    email = Column(String(20), unique=True)
    full_name = Column(String(20))
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role_id = Column(Integer, ForeignKey('role.id'))

    role = relationship("Role", back_populates="users")
    user_info = relationship("UserInfo", back_populates="user", uselist=False)
    vehicle = relationship("Vehicle", back_populates="user")

class UserInfo(Base):
    __tablename__ = 'user_info'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'),unique=True)
    city = Column(String(20))
    address = Column(Text)
    nic_number = Column(String(30), unique=True)
    phone_number = Column(String(30), unique=True)
    dob = Column(Date)
    pic_url = Column(Text)
    
    user = relationship("User", back_populates="user_info")


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True)
    description = Column(String(20))

    users = relationship("User", back_populates="role")


class Vehicle(Base):
    __tablename__ = 'vehicle'

    id = Column(Integer, primary_key=True, index=True)
    number_plate = Column(String(20), unique=True, index=True)
    vehicle_type = Column(String(10))
    vehicle_doc_url = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    user = relationship("User", back_populates="vehicle")