from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(...)
    id_account: str = Field(...)
    active: bool = Field(...)
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Name",
                "id_account": "6667907c95f0cd279feb07a2",
                "active": True,
                "username": "My username",
                "password": "My password"
            }
        }
    
class UpdateUserModel(BaseModel):
    name: Optional[str]
    id_account: Optional[str]
    active: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Name",
                "id_account": "6667907c95f0cd279feb07a2",
                "active": True,
                "username": "My username",
                "password": "My password"
            }
        }

def UserToDict(user: User) -> dict:
    return {
        "name": user.name,
        "id_account": user.id_account,
        "active": user.active,
        "username": user.username,
        "password": user.password
    }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
