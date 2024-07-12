from pydantic import BaseModel, Field


class Fields(BaseModel):
    id_entity_field: str = Field(...)
    obligatory: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity_field": "id_entity_field",
                "obligatory": "obligatory"
            }
        }


class UpdateFieldsModel(BaseModel):
    id_entity_field: str
    obligatory: str

    class Config:
        json_schema_extra = {
            "example": {
                "id_entity_field": "id_entity_field",
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
