from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel


class DataModel(BaseModel):
    data: List[Dict[str, Any]]

    class Config:
        # allow arbitrary values (ex.: NaN, Infinity, etc.)
        arbitrary_types_allowed = True
