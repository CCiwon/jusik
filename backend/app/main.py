from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.cache.cache_manager import cache_manager
from app.schedulers.data_scheduler import setup_scheduler, collect_fx, collect_indices
from app.routers import summary_bar, watchlist, sectors, events, ai_brief, futures


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await cache_manager.connect()

    # 스케줄러 시작
    sched = setup_scheduler()
    sched.start()

    # 첫 데이터 즉시 수집
    await collect_fx()
    await collect_indices()

    yield

    # Shutdown
    sched.shutdown(wait=False)
    await cache_manager.disconnect()
    await engine.dispose()


app = FastAPI(
    title="Korea-US Market Dashboard API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(summary_bar.router)
app.include_router(watchlist.router)
app.include_router(sectors.router)
app.include_router(events.router)
app.include_router(ai_brief.router)
app.include_router(futures.router)


@app.get("/health")
async def health():
    redis_ok = await cache_manager.ping()
    return {"status": "ok", "tz": settings.tz, "redis": redis_ok}
