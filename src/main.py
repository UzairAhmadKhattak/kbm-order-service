from fastapi import FastAPI
from src.accounts.routers import router
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse


load_dotenv()

app = FastAPI()

@app.get("/health", response_class=PlainTextResponse)
async def health_check():
    return "OK"
 
app.include_router(router, prefix='/api/v1')