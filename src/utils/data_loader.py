import pandas as pd
import os
from fastapi import status
from fastapi.responses import JSONResponse
from src.models.data_models import DataModel


def load_csv_data(file_name: str) -> DataModel:
    from src.state import is_scraping_completed

    file_path = os.path.join("data", file_name)

    if not os.path.exists(file_path):
        if not is_scraping_completed:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "message": "The web scraping process is ongoing. Please try again later."
                },
            )
        else:
            # If scraping has already completed, it means that an error occurred
            # in the process.
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "Data for the endpoint in question was not found."
                    "Please try scraping again or contact a project contributor."
                },
            )

    df = pd.read_csv(file_path)
    data_json = df.to_dict(orient="records")
    return DataModel(data=data_json)
