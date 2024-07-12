from pydantic import BaseModel, Field


class ActionType(BaseModel):
    name: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "active": True
            }
        }


class UpdateActionTypeModel(BaseModel):
    name: str
    active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
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
