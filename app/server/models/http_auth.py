from pydantic import BaseModel, Field


class HttpAuth(BaseModel):
    name: str = Field(...)
    host: str = Field(...)
    method: str = Field(...)
    id_http_auth_type: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "host": "host",
                "method": "method",
                "id_http_auth_type": "id_http_auth_type"
            }
        }


class UpdateHttpAuthModel(BaseModel):
    name: str
    host: str
    method: str
    id_http_auth_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "host": "host",
                "method": "method",
                "id_http_auth_type": "id_http_auth_type"
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
