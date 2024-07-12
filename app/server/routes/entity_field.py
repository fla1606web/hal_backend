from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.entity_field import (
    add_entity_field,
    delete_entity_field,
    retrieve_entity_field,
    retrieve_entity_fields,
    update_entity_field,
    retrieve_entity_fields_id_entity
)
from server.models.entity_field import (
    ErrorResponseModel,
    ResponseModel,
    EntityField,
    UpdateEntityFieldModel,
)

router = APIRouter()

@router.post("/", response_description="EntityField data added into the database")
async def add_entity_field_data(entity_field: EntityField = Body(...)):
    entity_field = jsonable_encoder(entity_field)
    new_entity_field = await add_entity_field(entity_field)
    return ResponseModel(new_entity_field, "EntityField added successfully.")

@router.get("/", response_description="EntityFields retrieved")
async def get_entity_field_fields():
    entity_field_fields = await retrieve_entity_fields()
    if entity_field_fields:
        return ResponseModel(entity_field_fields, "EntityFields data retrieved successfully")
    return ResponseModel(entity_field_fields, "Empty list returned")

@router.get("/{id}", response_description="EntityField data retrieved")
async def get_entity_field_data(id):
    entity_field = await retrieve_entity_field(id)
    if entity_field:
        return ResponseModel(entity_field, "EntityField data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "EntityField doesn't exist.")

@router.put("/{id}")
async def update_entity_field_data(id: str, req: UpdateEntityFieldModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_entity_field = await update_entity_field(id, req)
    if updated_entity_field:
        return ResponseModel(
            "EntityField with ID: {} name update is successful".format(id),
            "EntityField name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the entity_field data.",
    )

@router.delete("/{id}", response_description="EntityField data deleted from the database")
async def delete_entity_field_data(id: str):
    deleted_entity_field = await delete_entity_field(id)
    if deleted_entity_field:
        return ResponseModel(
            "EntityField with ID: {} removed".format(id), "EntityField deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "EntityField with id {0} doesn't exist".format(id)
    )

@router.get("/entity/{id}", response_description="EntityFields retrieved")
async def get_entity_field_fields_id_entity(id: str):
    entity_field_fields = await retrieve_entity_fields_id_entity(id)
    if entity_field_fields:
        return ResponseModel(entity_field_fields, "EntityFields data retrieved successfully")
    return ResponseModel(entity_field_fields, "Empty list returned")
