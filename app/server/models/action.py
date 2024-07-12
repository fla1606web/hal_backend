from pydantic import BaseModel, Field


class Action(BaseModel):
    name: str = Field(...)
    id_task: str = Field(...)
    id_action_type: str = Field(...)
    id_entity: str = Field(...)
    fields: str = Field(...)
    notifications: str = Field(...)
    id_http_request: str = Field(...)
    script: str = Field(...)
    id_action_next: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "id_task": "id_task",
                "id_action_type": "id_action_type",
                "id_entity": "id_entity",
                "fields": "fields",
                "notifications": "notifications",
                "id_http_request": "id_http_request",
                "script": "script",
                "id_action_next": "id_action_next",
                "active": True
            }
        }


class UpdateActionModel(BaseModel):
    name: str
    id_task: str
    id_action_type: str
    id_entity: str
    fields: str
    notifications: str
    id_http_request: str
    script: str
    id_action_next: str
    active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "id_task": "id_task",
                "id_action_type": "id_action_type",
                "id_entity": "id_entity",
                "fields": "fields",
                "notifications": "notifications",
                "id_http_request": "id_http_request",
                "script": "script",
                "id_action_next": "id_action_next",
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
