from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import dotenv_values

env = dotenv_values('.env')

DATABASE_URL = f"{env['DRIVER']}://{env['USERNAME']}:{env['PASSWORD']}@{env['HOST']}/{env['DATABASE']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
