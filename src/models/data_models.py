from pydantic import BaseModel
from typing import Any, List, Dict

class DataModel(BaseModel):
    data: List[Dict[str, Any]]

    class Config:
        # allow arbitrary values (ex.: NaN, Infinity, etc.)
        arbitrary_types_allowed = True