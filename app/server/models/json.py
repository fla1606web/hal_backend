from pydantic import BaseModel, Field


class Json(BaseModel):
    name: str = Field(...)
    data: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "data": "data"
            }
        }


class UpdateJsonModel(BaseModel):
    name: str
    data: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "data": "data"
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
