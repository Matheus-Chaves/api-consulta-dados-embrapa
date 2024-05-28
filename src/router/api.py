from fastapi import APIRouter
from src.router.v1 import auth, production, processing, commercialization, importation, exportation

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(production.router)
router.include_router(processing.router)
router.include_router(commercialization.router)
router.include_router(importation.router)
router.include_router(exportation.router)
