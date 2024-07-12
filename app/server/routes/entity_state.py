from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.entity_state import (
    add_entity_state,
    delete_entity_state,
    retrieve_entity_state,
    retrieve_entitys_state,
    update_entity_state,
)
from server.models.entity_state import (
    ErrorResponseModel,
    ResponseModel,
    EntityState,
    UpdateEntityStateModel,
)

router = APIRouter()


@router.post("/", response_description="Entity State data added into the database")
async def add_entity_state_data(entity_state: EntityState = Body(...)):
    entity_state = jsonable_encoder(entity_state)
    new_entity_state = await add_entity_state(entity_state)
    return ResponseModel(new_entity_state, "Entity State added successfully.")


@router.get("/", response_description="Entitys State retrieved")
async def get_entitys_state():
    entitys_state = await retrieve_entitys_state()
    if entitys_state:
        return ResponseModel(entitys_state, "Entitys State data retrieved successfully")
    return ResponseModel(entitys_state, "Empty list returned")


@router.get("/{id}", response_description="Entity State data retrieved")
async def get_entity_state_data(id):
    entity_state = await retrieve_entity_state(id)
    if entity_state:
        return ResponseModel(entity_state, "Entity State data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Plan doesn't exist.")


@router.put("/{id}")
async def update_entity_state_data(id: str, req: UpdateEntityStateModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_entity_state = await update_entity_state(id, req)
    if updated_entity_state:
        return ResponseModel(
            "Entity State with ID: {} name update is successful".format(id),
            "Entity State name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Plan data.",
    )


@router.delete("/{id}", response_description="Entity State data deleted from the database")
async def delete_entity_state_data(id: str):
    deleted_entity_state = await delete_entity_state(id)
    if deleted_entity_state:
        return ResponseModel(
            "Entity State with ID: {} removed".format(
                id), "Entity State deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Entity State with id {0} doesn't exist".format(
            id)
    )
