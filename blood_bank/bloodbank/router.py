from fastapi import APIRouter

from .routers import health

router = APIRouter(prefix="/bloodbank")

router.include_router(health.router)