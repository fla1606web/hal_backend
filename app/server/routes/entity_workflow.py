from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.entity_workflow import (
    add_entity_workflow,
    delete_entity_workflow,
    retrieve_entity_workflow,
    retrieve_entitys_workflow,
    update_entity_workflow,
)
from server.models.entity_workflow import (
    ErrorResponseModel,
    ResponseModel,
    EntityWorkflow,
    UpdateEntityWorkflowModel,
)

router = APIRouter()


@router.post("/", response_description="EntityField data added into the database")
async def add_entity_workflow_data(entity_workflow: EntityWorkflow = Body(...)):
    entity_workflow = jsonable_encoder(entity_workflow)
    new_entity_workflow = await add_entity_workflow(entity_workflow)
    return ResponseModel(new_entity_workflow, "EntityWorkflow added successfully.")


@router.get("/", response_description="Entity Workflow retrieved")
async def get_entitys_workflow():
    entitys_workflow = await retrieve_entitys_workflow()
    if entitys_workflow:
        return ResponseModel(entitys_workflow, "Entity Workflow data retrieved successfully")
    return ResponseModel(entitys_workflow, "Empty list returned")


@router.get("/{id}", response_description="EntityField data retrieved")
async def get_entity_workflow_data(id):
    entity_workflow = await retrieve_entity_workflow(id)
    if entity_workflow:
        return ResponseModel(entity_workflow, "Entity Workflow data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Entity Workflow doesn't exist.")


@router.put("/{id}")
async def update_entity_workflow_data(id: str, req: UpdateEntityWorkflowModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_entity_workflow = await update_entity_workflow(id, req)
    if updated_entity_workflow:
        return ResponseModel(
            "Entity Workflow with ID: {} name update is successful".format(id),
            "Entity Workflow name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Entity Workflow data.",
    )


@router.delete("/{id}", response_description="Entity Workflow data deleted from the database")
async def delete_entity_workflow_data(id: str):
    deleted_entity_workflow = await delete_entity_workflow(id)
    if deleted_entity_workflow:
        return ResponseModel(
            "Entity Workflow with ID: {} removed".format(
                id), "Entity Workflow deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Entity Workflow with id {0} doesn't exist".format(
            id)
    )
