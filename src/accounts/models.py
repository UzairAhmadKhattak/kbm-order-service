from sqlalchemy import Column, Integer, String, ForeignKey,Date,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

metadata = Base.metadata

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    full_name = Column(String)
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
    city = Column(String)
    address = Column(String)
    nic_number = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    date = Column(Date)
    pic_url = Column(String)
    
    user = relationship("User", back_populates="user_info")


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    users = relationship("User", back_populates="role")


class Vehicle(Base):
    __tablename__ = 'vehicle'

    id = Column(Integer, primary_key=True, index=True)
    number_plate = Column(String, unique=True, index=True)
    vehicle_type = Column(String)
    vehicle_doc_url = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    user = relationship("User", back_populates="vehicle")