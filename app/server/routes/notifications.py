from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.notifications import (
    add_notification,
    delete_notification,
    retrieve_notification,
    retrieve_notifications,
    update_notification,
)
from server.models.notifications import (
    ErrorResponseModel,
    ResponseModel,
    Notifications,
    UpdateNotificationsModel,
)

router = APIRouter()


@router.post("/", response_description="Notification data added into the database")
async def add_notification_data(notification: Notifications = Body(...)):
    notification = jsonable_encoder(notification)
    new_notification = await add_notification(notification)
    return ResponseModel(new_notification, "Notification added successfully.")


@router.get("/", response_description="Notifications retrieved")
async def get_notifications():
    notifications = await retrieve_notifications()
    if notifications:
        return ResponseModel(notifications, "Notifications data retrieved successfully")
    return ResponseModel(notifications, "Empty list returned")


@router.get("/{id}", response_description="Notification data retrieved")
async def get_notification_data(id):
    notification = await retrieve_notification(id)
    if notification:
        return ResponseModel(notification, "Notification data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Notification doesn't exist.")


@router.put("/{id}")
async def update_notification_data(id: str, req: UpdateNotificationsModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_notification = await update_notification(id, req)
    if updated_notification:
        return ResponseModel(
            "Notification with ID: {} name update is successful".format(id),
            "Notification name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Notification data.",
    )


@router.delete("/{id}", response_description="Notification data deleted from the database")
async def delete_notification_data(id: str):
    deleted_notification = await delete_notification(id)
    if deleted_notification:
        return ResponseModel(
            "Notification with ID: {} removed".format(
                id), "Account deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Notification with id {0} doesn't exist".format(
            id)
    )
