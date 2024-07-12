from typing import Optional

from pydantic import BaseModel, Field

class EntityField(BaseModel):
    id_entity: str = Field(...)
    name: str = Field(...)
    column_name: str = Field(...)
    id_entity_type: str = Field(...)
    color: str = Field(...)
    icon: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity": "6667907c95f0cd279feb07a2",
                "name": "Nombre",
                "column_name": "nombre",
                "id_entity_type": "6667907c95f0cd279feb07a2",
                "color": "#f3f3f3",
                "icon": "fa-people",
                "active": True
            }
        }

class UpdateEntityFieldModel(BaseModel):
    id_entity: Optional[str]
    name: Optional[str]
    column_name: Optional[str]
    id_entity_type: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    active: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity": "6667907c95f0cd279feb07a2",
                "name": "Nombre",
                "column_name": "nombre",
                "id_entity_type": "6667907c95f0cd279feb07a2",
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
