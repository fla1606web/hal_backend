from pydantic import BaseModel, Field


class EntityWorkflow(BaseModel):
    id_entity: str = Field(...)
    id_entity_state_origin: str = Field(...)
    id_entity_state_destination: str = Field(...)
    name_action: str = Field(...)
    color: str = Field(...)
    icon: str = Field(...)
    fields: str = Field(...)
    roles: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity": "id_entity",
                "id_entity_state_origin": "id_entity_state_origin",
                "id_entity_state_destination": "id_entity_state_origin",
                "name_action": "name_action",
                "color": "color",
                "icon": "icon",
                "fields": "fields",
                "roles": "roles",
                "active": True
            }
        }


class UpdateEntityWorkflowModel(BaseModel):
    id_entity: str
    id_entity_state_origin: str
    id_entity_state_destination: str
    name_action: str
    color: str
    icon: str
    fields: str
    roles: str
    active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity": "id_entity",
                "id_entity_state_origin": "id_entity_state_origin",
                "id_entity_state_destination": "id_entity_state_origin",
                "name_action": "name_action",
                "color": "color",
                "icon": "icon",
                "fields": "fields",
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
