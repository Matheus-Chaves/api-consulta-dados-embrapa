from fastapi import APIRouter, HTTPException, Depends
from src.utils.data_loader import load_csv_data
from src.config.responses import RESPONSES
from src.auth import get_current_user


def create_route(router: APIRouter, endpoint: str, config: dict):
    async def get_data():
        try:
            file_name = config["file_name"]
            return load_csv_data(file_name)
        except HTTPException as e:
            raise e

    router.add_api_route(
        endpoint,
        get_data,
        summary=config["summary"],
        description=config["description"],
        methods=["GET"],
        responses=RESPONSES,
        dependencies=[Depends(get_current_user)]
    )
