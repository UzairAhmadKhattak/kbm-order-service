from fastapi import FastAPI
from src.accounts.routers import router
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()
app.include_router(router, prefix='/api/v1', tags=['v1'])

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)