from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.action import (
    add_action,
    delete_action,
    retrieve_action,
    retrieve_actions,
    update_action,
)
from server.models.action import (
    ErrorResponseModel,
    ResponseModel,
    Action,
    UpdateActionModel,
)

router = APIRouter()


@router.post("/", response_description="Action data added into the database")
async def add_action_data(action: Action = Body(...)):
    action = jsonable_encoder(action)
    new_action = await add_action(action)
    return ResponseModel(new_action, "Action added successfully.")


@router.get("/", response_description="Action retrieved")
async def get_actions():
    actions = await retrieve_actions()
    if actions:
        return ResponseModel(actions, "Action data retrieved successfully")
    return ResponseModel(actions, "Empty list returned")


@router.get("/{id}", response_description="Action data retrieved")
async def get_action_data(id):
    action = await retrieve_action(id)
    if action:
        return ResponseModel(action, "Action data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Action doesn't exist.")


@router.put("/{id}")
async def update_action_data(id: str, req: UpdateActionModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_action = await update_action(id, req)
    if updated_action:
        return ResponseModel(
            "Action with ID: {} name update is successful".format(id),
            "Action name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the action data.",
    )


@router.delete("/{id}", response_description="Action data deleted from the database")
async def delete_action_data(id: str):
    deleted_action = await delete_action(id)
    if deleted_action:
        return ResponseModel(
            "Action with ID: {} removed".format(
                id), "Action deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Action with id {0} doesn't exist".format(
            id)
    )
