from fastapi import APIRouter

from src.router.v1 import auth
from src.router.v1 import commercialization
from src.router.v1 import exportation
from src.router.v1 import importation
from src.router.v1 import processing
from src.router.v1 import production

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(production.router)
router.include_router(processing.router)
router.include_router(commercialization.router)
router.include_router(importation.router)
router.include_router(exportation.router)
