from fastapi import APIRouter

from src.config.processing import ROUTE_CONFIG as ROUTE
from src.utils.router import create_route

router = APIRouter(prefix=ROUTE["base_path"], tags=ROUTE["tags"])

for endpoint, config in ROUTE["endpoints"].items():
    create_route(router, endpoint, config)
