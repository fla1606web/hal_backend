from pydantic import BaseModel, Field


class Template(BaseModel):
    name: str = Field(...)
    id_template_type: str = Field(...)
    template: str = Field(...)
    active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "id_template_type": "id_template_type",
                "template": "template",
                "active": True
            }
        }


class UpdateTemplateModel(BaseModel):
    name: str
    id_template_type: str
    template: str
    active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name",
                "id_template_type": "id_template_type",
                "template": "template",
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
