from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.action_type import (
    add_action_type,
    delete_action_type,
    retrieve_action_type,
    retrieve_actions_type,
    update_action_type,
)
from server.models.action_type import (
    ErrorResponseModel,
    ResponseModel,
    ActionType,
    UpdateActionTypeModel,
)

router = APIRouter()


@router.post("/", response_description="Action Type data added into the database")
async def add_action_type_data(action_type: ActionType = Body(...)):
    action_type = jsonable_encoder(action_type)
    new_action_type = await add_action_type(action_type)
    return ResponseModel(new_action_type, "Action Type added successfully.")


@router.get("/", response_description="Action Type retrieved")
async def get_actions_type():
    actions_type = await retrieve_actions_type()
    if actions_type:
        return ResponseModel(actions_type, "Actions Type data retrieved successfully")
    return ResponseModel(actions_type, "Empty list returned")


@router.get("/{id}", response_description="Notification Type data retrieved")
async def get_action_type_data(id):
    action_type = await retrieve_action_type(id)
    if action_type:
        return ResponseModel(action_type, "Action Type data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Action type doesn't exist.")


@router.put("/{id}")
async def update_action_type_data(id: str, req: UpdateActionTypeModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_action_type = await update_action_type(id, req)
    if updated_action_type:
        return ResponseModel(
            "Action Type with ID: {} name update is successful".format(
                id),
            "Action Type name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Action Type data.",
    )


@router.delete("/{id}", response_description="Action Type data deleted from the database")
async def delete_action_type_data(id: str):
    deleted_action_type = await delete_action_type(id)
    if deleted_action_type:
        return ResponseModel(
            "Action Type with ID: {} removed".format(
                id), "Action Type deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Action Type with id {0} doesn't exist".format(
            id)
    )
