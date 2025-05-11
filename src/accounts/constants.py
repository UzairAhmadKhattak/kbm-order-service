from enum import Enum

class UserConstants(Enum):
    USER_EXISTS = "User already exists"

    CUSTOMER_ROLE = {"name":'customer','description':'this is a customer role'}
    DELIVERER_ROLE = {'name':'deliverer','description':'this is a deliverer role'}
    SUPER_ADMIN = {'name':'super_admin','description':'this is a super admin role'}