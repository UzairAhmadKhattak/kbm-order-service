from fastapi import FastAPI
from src.accounts.routers import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(router, prefix='/api/v1')