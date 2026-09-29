from fastapi import APIRouter

from .routers import (auth, health, blood_group, donor, doctor, staff, patient, blood_component, donation, blood_unit,)

router = APIRouter(prefix="/bloodbank")

router.include_router(health.router)
router.include_router(auth.router)
router.include_router(blood_group.router)
router.include_router(donor.router)
router.include_router(doctor.router)
router.include_router(staff.router)
router.include_router(patient.router)
router.include_router(blood_component.router)
router.include_router(donation.router)
router.include_router(blood_unit.router)