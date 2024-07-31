from pydantic import BaseModel, Field


class Account(BaseModel):
    name: str = Field(...)
    id_plan: str = Field(...)
    database_host: str = Field(...)
    database_name: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Company",
                "id_plan": "id_plan",
                "database_host": "localhost",
                "database_name": "my_company",
                "active": True
            }
        }


class UpdateAccountModel(BaseModel):
    name: str = Field(...)
    id_plan: str = Field(...)
    database_host: str = Field(...)
    database_name: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Company",
                "id_plan": "id_plan",
                "database_host": "localhost",
                "database_name": "my_company",
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

