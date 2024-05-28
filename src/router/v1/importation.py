from fastapi import APIRouter
from src.utils.router import create_route
from src.config.importation import ROUTE_CONFIG as ROUTE

router = APIRouter(prefix=ROUTE["base_path"], tags=ROUTE["tags"])

for endpoint, config in ROUTE["endpoints"].items():
    create_route(router, endpoint, config)