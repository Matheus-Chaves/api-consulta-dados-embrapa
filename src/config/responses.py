from typing import Any
from typing import Dict

from fastapi import status
from pydantic import BaseModel

from src.models.data_models import DataModel


class SuccessResponse(BaseModel):
    data: DataModel


class ErrorResponse(BaseModel):
    message: str


RESPONSES: Dict[str, Dict[str, Any]] = {
    status.HTTP_200_OK: {
        "description": "The data was obtained successfully!",
        "model": SuccessResponse,
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "id": 5,
                            "id_pai": 3,
                            "produto": "Nome do produto",
                            "ano1_quantidade": "123.456.789",
                            "ano2_quantidade": "123.456.789",
                        }
                    ]
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorResponse,
        "description": "User unauthorized.",
    },
    # status.HTTP_403_FORBIDDEN: {
    #     "model": ErrorResponse,
    #     "description": "Not enough privileges",
    # },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponse,
        "description": "Data for the endpoint in question was not found."
        "Please try scraping again or contact a project contributor.",
    },
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "model": ErrorResponse,
        "description": "The web scraping process is ongoing. Please try again later.",
    },
}
