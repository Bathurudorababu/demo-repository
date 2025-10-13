from typing import Any, Optional
from pydantic import BaseModel


class OutModel(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Data retrieved successfully",
                "data": {},
            }
        }
