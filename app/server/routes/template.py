from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.template import (
    add_template,
    delete_template,
    retrieve_template,
    retrieve_templates,
    update_template,
)
from server.models.template import (
    ErrorResponseModel,
    ResponseModel,
    Template,
    UpdateTemplateModel,
)

router = APIRouter()


@router.post("/", response_description="Template data added into the database")
async def add_template_data(template: Template = Body(...)):
    template = jsonable_encoder(template)
    new_template = await add_template(template)
    return ResponseModel(new_template, "Template added successfully.")


@router.get("/", response_description="Templates retrieved")
async def get_templates():
    templates = await retrieve_templates()
    if templates:
        return ResponseModel(templates, "Templates data retrieved successfully")
    return ResponseModel(templates, "Empty list returned")


@router.get("/{id}", response_description="Template data retrieved")
async def get_template_data(id):
    template = await retrieve_template(id)
    if template:
        return ResponseModel(template, "Template data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Account doesn't exist.")


@router.put("/{id}")
async def update_template_data(id: str, req: UpdateTemplateModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_template = await update_template(id, req)
    if updated_template:
        return ResponseModel(
            "Template with ID: {} name update is successful".format(id),
            "Template name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error Template the account data.",
    )


@router.delete("/{id}", response_description="Template data deleted from the database")
async def delete_template_data(id: str):
    deleted_template = await delete_template(id)
    if deleted_template:
        return ResponseModel(
            "Template with ID: {} removed".format(
                id), "Template deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Template with id {0} doesn't exist".format(
            id)
    )
