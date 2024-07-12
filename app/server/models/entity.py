from typing import Optional, List

from pydantic import BaseModel, Field, Json

class Entity(BaseModel):
    name: str = Field(...)
    id_account: str = Field(...)
    collection_name: str = Field(...)
    color: str = Field(...)
    icon: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Clients",
                "id_account": "6667907c95f0cd279feb07a2",
                "collection_name": "client",
                "color": "#f3f3f3",
                "icon": "fa-people",
                "active": True
            }
        }

class UpdateEntityModel(BaseModel):
    name: Optional[str]
    id_account: Optional[str]
    collection_name: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    active: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Clients",
                "id_account": "6667907c95f0cd279feb07a2",
                "collection_name": "client",
                "color": "#f3f3f3",
                "icon": "fa-people",
                "active": True
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
