from pydantic import BaseModel, Field


class UserAccountRol(BaseModel):
    id_account: str = Field(...)
    name: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_account": "id_account",
                "name": "name",
                "active": True
            }
        }


class UpdateUserAccountRol(BaseModel):
    id_account: str
    name: str
    active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id_account": "id_account",
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
