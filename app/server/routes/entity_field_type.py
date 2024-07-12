from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.entity_field_type import (
    add_entity_field_type,
    delete_entity_field_type,
    retrieve_entity_field_type,
    retrieve_entitys_field_type,
    update_entity_field_type,
)
from server.models.entity_field_type import (
    ErrorResponseModel,
    ResponseModel,
    EntityFieldType,
    UpdateEntityFieldTypeModel,
)

router = APIRouter()


@router.post("/", response_description="Plan data added into the database")
async def add_entity_field_type_data(entity_field_type: EntityFieldType = Body(...)):
    entity_field_type = jsonable_encoder(entity_field_type)
    new_entity_field_type = await add_entity_field_type(entity_field_type)
    return ResponseModel(new_entity_field_type, "Entity Field Type added successfully.")


@router.get("/", response_description="Entitys Field Type retrieved")
async def get_entitys_field_type():
    entitys_field_type = await retrieve_entitys_field_type()
    if entitys_field_type:
        return ResponseModel(entitys_field_type, "Entitys Field Type data retrieved successfully")
    return ResponseModel(entitys_field_type, "Empty list returned")


@router.get("/{id}", response_description="Entity Field Type data retrieved")
async def get__data(id):
    entity_field_type = await retrieve_entity_field_type(id)
    if entity_field_type:
        return ResponseModel(entity_field_type, "Entity Field Type data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Entity Field Type doesn't exist.")


@router.put("/{id}")
async def update_entity_field_type_data(id: str, req: UpdateEntityFieldTypeModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_entity_field_type = await update_entity_field_type(id, req)
    if updated_entity_field_type:
        return ResponseModel(
            "Entity Field Type with ID: {} name update is successful".format(
                id),
            "Entity Field Type name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Entity Field Type data.",
    )


@router.delete("/{id}", response_description="Entity Field Type data deleted from the database")
async def delete_entity_field_type_data(id: str):
    deleted_entity_field_type = await delete_entity_field_type(id)
    if deleted_entity_field_type:
        return ResponseModel(
            "Entity Field Type with ID: {} removed".format(
                id), "Entity Field Type deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Entity Field Type with id {0} doesn't exist".format(
            id)
    )
