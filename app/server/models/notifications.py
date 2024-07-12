from pydantic import BaseModel, Field
from typing import Optional


class Notifications(BaseModel):
    mails_to_notify: str = Field(...)
    phones_to_notify: str = Field(...)
    users_to_notify: str = Field(...)
    id_tamplate_mail: str = Field(...)
    id_tamplate_whatsapp: str = Field(...)
    id_tamplate_push: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "mails_to_notify": "mails_to_notify",
                "phones_to_notify": "phones_to_notify",
                "users_to_notify": "users_to_notify",
                "id_tamplate_mail": "id_tamplate_mail",
                "id_tamplate_whatsapp": "id_tamplate_whatsapp",
                "id_tamplate_push": "id_tamplate_push"
            }
        }


class UpdateNotificationsModel(BaseModel):
    mails_to_notify: Optional[str]
    phones_to_notify: Optional[str]
    users_to_notify: Optional[str]
    id_tamplate_mail: Optional[str]
    id_tamplate_whatsapp: Optional[str]
    id_tamplate_push: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "mails_to_notify": "mails_to_notify",
                "phones_to_notify": "phones_to_notify",
                "users_to_notify": "users_to_notify",
                "id_tamplate_mail": "id_tamplate_mail",
                "id_tamplate_whatsapp": "id_tamplate_whatsapp",
                "id_tamplate_push": "id_tamplate_push"
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
