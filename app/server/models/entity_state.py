from pydantic import BaseModel, Field


class EntityState(BaseModel):
    id_entity: str = Field(...)
    name: str = Field(...)
    color: str = Field(...)
    icon: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity": "id_entity",
                "name": "name",
                "color": "#f030303",
                "icon": "fa-people",
                "active": True
            }
        }


class UpdateEntityStateModel(BaseModel):
    id_entity: str
    name: str
    color: str
    icon: str
    active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity": "id_entity",
                "name": "name",
                "color": "#f030303",
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
