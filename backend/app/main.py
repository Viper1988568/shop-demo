"""川香小馆 API 入口。

启动方式（backend/ 目录下）：uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import menu, orders


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="川香小馆 API", version="1.0.0", lifespan=lifespan)

# 开发期放开跨域：前端直连或走 vite proxy 都能用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu.router)
app.include_router(orders.router)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}
