from fastapi import APIRouter

from .routers import auth, health, blood_group, donor

router = APIRouter(prefix="/bloodbank")

router.include_router(health.router)
router.include_router(auth.router)
router.include_router(blood_group.router)
router.include_router(donor.router)