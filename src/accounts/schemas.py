from pydantic import (BaseModel,
                      Field,
                      EmailStr,
                      constr)
from datetime import date
from enum import Enum
from fastapi import Form
from typing import Type


class UserBase(BaseModel):
    username : str
    email : EmailStr
    full_name : str


class UserCreate(UserBase):
    password : str = Field(..., min_length=8, max_length=20)


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class MoreUserInfo(BaseModel):
    city: str
    address: str
    nic_number: str
    phone_number: str
    dob: date


class VehicleType(str, Enum):
    CAR = "car"
    BIKE = "bike"
    TRUCK = "truck"


class Vehicle(BaseModel):
    number_plate: str
    vehicle_type: str


class DelivererRegister(UserCreate, MoreUserInfo, Vehicle):

    @property
    def vehicle(self) -> Vehicle:
        return Vehicle(number_plate=self.number_plate,
                       vehicle_type=self.vehicle_type)

    @property
    def user(self) -> UserCreate:
        return UserCreate(username=self.username,
                          email=self.email,
                          full_name=self.full_name,
                          password=self.password)
    @property
    def more_user_info(self) -> MoreUserInfo:
        return MoreUserInfo(city=self.city,
                            address=self.address,
                            nic_number=self.nic_number,
                            phone_number=self.phone_number,
                            dob=self.dob)


class UserSuccessResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Successfully Register the user"
            }
        }

