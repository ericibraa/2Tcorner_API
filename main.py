from fastapi import FastAPI
from dotenv import dotenv_values
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from routes.api import router
from functools import lru_cache
from src.database.mongo import init_mongo, close_mongo
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongo(app)
    yield
    await close_mongo(app)

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)



