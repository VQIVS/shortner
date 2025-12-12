from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from shortner.handlers.link import router as link_router, redirect_router
import os
import uvicorn

import shortner.handlers.link as link_handler
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/shortner"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  
    future=True,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    
    print("Shutting down...")
    await engine.dispose()
    print("Database connection closed")


app = FastAPI(
    title="Link Shortener API",
    description="A simple link shortener API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


link_handler.get_db_dependency = get_db

app.include_router(link_router, prefix="/api")
app.include_router(redirect_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
