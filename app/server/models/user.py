from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id_account: str = Field(...)
    id_user_account_rol: str = Field(...)
    user: str = Field(...)
    password: str = Field(...)
    mail: str = Field(...)
    name: str = Field(...)
    last_name: str = Field(...)
    telephone: str = Field(...)
    lang: str = Field(...)
    time_zone: str = Field(...)
    token_firebase: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_account": "id_account",
                "id_user_account_rol": "id_user_account_rol",
                "user": "user",
                "password": "password",
                "mail": "mail",
                "name": "name",
                "last_name": "last_name",
                "telephone": "telephone",
                "lang": "lang",
                "time_zone": "time_zone",
                "token_firebase": "token_firebase",
                "active": True
            }
        }


class UpdateUserModel(BaseModel):
    id_account: Optional[str]
    id_user_account_rol: Optional[str]
    user: Optional[str]
    password: Optional[str]
    mail: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    telephone: int
    lang: Optional[str]
    time_zone: Optional[str]
    token_firebase: Optional[str]
    active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id_account": "id_account",
                "id_user_account_rol": "id_user_account_rol",
                "user": "user",
                "password": "password",
                "mail": "mail",
                "name": "name",
                "last_name": "last_name",
                "telephone": "telephone",
                "lang": "lang",
                "time_zone": "time_zone",
                "token_firebase": "token_firebase",
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
