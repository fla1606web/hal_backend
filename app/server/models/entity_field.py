from typing import Optional

from pydantic import BaseModel, Field


class EntityField(BaseModel):
    id_entity: str = Field(...)
    name: str = Field(...)
    field_name: str = Field(...)
    id_entity_field_type: str = Field(...)
    id_entity_relation: str = Field(...)
    entity_relation_field_name: str = Field(...)
    required: str = Field(...)
    order: str = Field(...)
    minimun: str = Field(...)
    maximun: str = Field(...)
    options: str = Field(...)
    roles: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity": "6667907c95f0cd279feb07a2",
                "name": "Nombre",
                "field_name": "nombre",
                "id_entity_field_type": "6667907c95f0cd279feb07a2",
                "id_entity_relation": "id_entity_relation",
                "entity_relation_field_name": "entity_relation_field_name",
                "required": "required",
                "order": "order",
                "minimun": "minimun",
                "maximun": "maximun",
                "options": "options",
                "roles": "roles",
                "active": True
            }
        }


class UpdateEntityFieldModel(BaseModel):
    id_entity: Optional[str]
    name: Optional[str]
    field_name: Optional[str]
    id_entity_field_type: Optional[str]
    id_entity_relation: Optional[str]
    entity_relation_field_name: Optional[str]
    required: Optional[str]
    order: Optional[str]
    minimun: Optional[str]
    maximun: Optional[str]
    options: Optional[str]
    roles: Optional[str]
    active: Optional[bool]

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity": "6667907c95f0cd279feb07a2",
                "name": "Nombre",
                "field_name": "nombre",
                "id_entity_field_type": "6667907c95f0cd279feb07a2",
                "id_entity_relation": "id_entity_relation",
                "entity_relation_field_name": "entity_relation_field_name",
                "required": "required",
                "order": "order",
                "minimun": "minimun",
                "maximun": "maximun",
                "options": "options",
                "roles": "roles",
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
