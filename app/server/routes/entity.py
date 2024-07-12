from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.entity import (
    add_entity,
    delete_entity,
    retrieve_entity,
    retrieve_entities,
    retrieve_entities_account,
    update_entity,
)
from server.models.entity import (
    ErrorResponseModel,
    ResponseModel,
    Entity,
    UpdateEntityModel,
)

router = APIRouter()

@router.post("/", response_description="Entity data added into the database")
async def add_entity_data(entity: Entity = Body(...)):
    entity = jsonable_encoder(entity)
    new_entity = await add_entity(entity)
    return ResponseModel(new_entity, "Entity added successfully.")

@router.get("/account/{id}", response_description="Entities retrieved")
async def get_entities(id):
    entities = await retrieve_entities_account(id)
    if entities:
        print(entities)
        return ResponseModel(entities, "Entities data retrieved successfully")
    return ResponseModel(entities, "Empty list returned")

@router.get("/", response_description="Entities retrieved")
async def get_entities():
    print("pase por aca 1")
    entities = await retrieve_entities()
    if entities:
        print(entities)
        return ResponseModel(entities, "Entities data retrieved successfully")
    return ResponseModel(entities, "Empty list returned")

@router.get("/{id}", response_description="Entity data retrieved")
async def get_entity_data(id):
    entity = await retrieve_entity(id)
    if entity:
        return ResponseModel(entity, "Entity data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Entity doesn't exist.")

@router.put("/{id}")
async def update_entity_data(id: str):
    print("entro")
    req = {k: v for k, v in req.dict().items() if v is not None}
    print(req)
    updated_entity = await update_entity(id, req)
    if updated_entity:
        return ResponseModel(
            "Entity with ID: {} name update is successful".format(id),
            "Entity name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the entity data.",
    )

@router.delete("/{id}", response_description="Entity data deleted from the database")
async def delete_entity_data(id: str):
    deleted_entity = await delete_entity(id)
    if deleted_entity:
        return ResponseModel(
            "Entity with ID: {} removed".format(id), "Entity deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Entity with id {0} doesn't exist".format(id)
    )
