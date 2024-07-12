from pydantic import BaseModel, Field
from typing import Optional


class HttpRequest(BaseModel):
    name: str = Field(...)
    host: str = Field(...)
    method: str = Field(...)
    id_http_auth: str = Field(...)
    header: str = Field(...)
    query_string: str = Field(...)
    body_type: str = Field(...)
    content_type: str = Field(...)
    request: str = Field(...)
    response: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "host": "host",
                "method": "method",
                "id_http_auth": "id_http_auth",
                "header": "header",
                "query_string": "query_string",
                "body_type": "body_type",
                "content_type": "content_type",
                "request": "request",
                "response": "response"
            }
        }


class UpdateHttpRequestModel(BaseModel):
    name: Optional[str]
    host: Optional[str]
    method: Optional[str]
    id_http_auth: Optional[str]
    header: Optional[str]
    query_string: Optional[str]
    body_type: Optional[str]
    content_type: Optional[str]
    request: Optional[str]
    response: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "host": "host",
                "method": "method",
                "id_http_auth": "id_http_auth",
                "header": "header",
                "query_string": "query_string",
                "body_type": "body_type",
                "content_type": "content_type",
                "request": "request",
                "response": "response"
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
