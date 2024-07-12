from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.notification_type import (
    add_notification_type,
    delete_notification_type,
    retrieve_notification_type,
    retrieve_notifications_type,
    update_notification_type,
)
from server.models.notification_type import (
    ErrorResponseModel,
    ResponseModel,
    NotificationType,
    UpdateNotificationTypeModel,
)

router = APIRouter()


@router.post("/", response_description="Notification Type data added into the database")
async def add_notification_type_data(notification_type: NotificationType = Body(...)):
    notification_type = jsonable_encoder(notification_type)
    new_notification_type = await add_notification_type(notification_type)
    return ResponseModel(new_notification_type, "Notification Type added successfully.")


@router.get("/", response_description="Notifications Type retrieved")
async def get_notifications_type():
    notifications_type = await retrieve_notifications_type()
    if notifications_type:
        return ResponseModel(notifications_type, "Notifications Type data retrieved successfully")
    return ResponseModel(notifications_type, "Empty list returned")


@router.get("/{id}", response_description="Notification Type data retrieved")
async def get_notification_type_data(id):
    notification_type = await retrieve_notification_type(id)
    if notification_type:
        return ResponseModel(notification_type, "Notification Type data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Notification doesn't exist.")


@router.put("/{id}")
async def update_notification_type_data(id: str, req: UpdateNotificationTypeModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_notification_type = await update_notification_type(id, req)
    if updated_notification_type:
        return ResponseModel(
            "Notification Type with ID: {} name update is successful".format(
                id),
            "Notification Type name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Notification Type data.",
    )


@router.delete("/{id}", response_description="Notification data deleted from the database")
async def delete_notification_type_data(id: str):
    deleted_notification_type = await delete_notification_type(id)
    if deleted_notification_type:
        return ResponseModel(
            "Notification Type with ID: {} removed".format(
                id), "Account deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Notification Type with id {0} doesn't exist".format(
            id)
    )
