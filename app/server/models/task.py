from pydantic import BaseModel, Field


class Task(BaseModel):
    name: str = Field(...)
    id_entity: str = Field(...)
    id_task_type: str = Field(...)
    expression: str = Field(...)
    cron: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "id_entity": "id_entity",
                "id_task_type": "id_task_type",
                "expression": "expression",
                "cron": "cron",
                "active": True
            }
        }


class UpdateTaskModel(BaseModel):
    name: str
    id_entity: str
    id_task_type: str
    expression: str
    cron: str
    active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "id_entity": "id_entity",
                "id_task_type": "id_task_type",
                "expression": "expression",
                "cron": "cron",
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
