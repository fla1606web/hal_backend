from pydantic import BaseModel, Field


class JsonData(BaseModel):
    name: str = Field(...)
    id_json_type_data: str = Field(...)
    value_default: str = Field(...)
    obligatory: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "id_json_type_data": "id_json_type_data",
                "value_default": "value_default",
                "obligatory": "obligatory"
            }
        }


class UpdateJsonDataModel(BaseModel):
    name: str
    id_json_type_data: str
    value_default: str
    obligatory: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "id_json_type_data": "id_json_type_data",
                "value_default": "value_default",
                "obligatory": "obligatory"
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
