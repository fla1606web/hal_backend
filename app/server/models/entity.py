from typing import Optional

from pydantic import BaseModel, Field


class Entity(BaseModel):
    id_account: str = Field(...)
    name: str = Field(...)
    table_name: str = Field(...)
    color: str = Field(...)
    icon: str = Field(...)
    roles: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_account": "6667907c95f0cd279feb07a2",
                "name": "Clients",
                "table_name": "client",
                "color": "#f3f3f3",
                "icon": "fa-people",
                "roles": "rol",
                "active": True
            }
        }


class UpdateEntityModel(BaseModel):
    id_account: Optional[str]
    name: Optional[str]
    table_name: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    roles: Optional[str]
    active: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "id_account": "6667907c95f0cd279feb07a2",
                "name": "Clients",
                "table_name": "client",
                "color": "#f3f3f3",
                "icon": "fa-people",
                "roles": "rol",
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
