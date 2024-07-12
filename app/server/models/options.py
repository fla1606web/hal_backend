from pydantic import BaseModel, Field


class Options(BaseModel):
    name: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name"
            }
        }


class UpdateOptionsModel(BaseModel):
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
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
