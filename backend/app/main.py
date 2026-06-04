from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import get_settings
from backend.app.db.database import init_db
from backend.app.api.routes import auth, room, design, furniture, cost, house, lighting, feng_shui, seasonal, pet_friendly, walkthrough_3d

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-Powered Room Redesign with AR Visualization, Furniture Recommendation, and Cost Estimation",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(room.router, prefix=API_PREFIX)
app.include_router(design.router, prefix=API_PREFIX)
app.include_router(furniture.router, prefix=API_PREFIX)
app.include_router(cost.router, prefix=API_PREFIX)
app.include_router(house.router, prefix=API_PREFIX)
app.include_router(lighting.router, prefix=API_PREFIX)
app.include_router(feng_shui.router, prefix=API_PREFIX)
app.include_router(seasonal.router, prefix=API_PREFIX)
app.include_router(pet_friendly.router, prefix=API_PREFIX)
app.include_router(walkthrough_3d.router, prefix=API_PREFIX)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
