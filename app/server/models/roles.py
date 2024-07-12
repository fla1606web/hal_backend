from pydantic import BaseModel, Field


class Roles(BaseModel):
    id_user: str = Field(...)
    view: str = Field(...)
    create: str = Field(...)
    modify: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_user": "id_user",
                "view": "view",
                "create": "create",
                "modify": "modify"
            }
        }


class UpdateRolesModel(BaseModel):
    id_user: str
    view: str
    create: str
    modify: str

    class Config:
        json_schema_extra = {
            "example": {
                "id_user": "id_user",
                "view": "view",
                "create": "create",
                "modify": "modify"
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
