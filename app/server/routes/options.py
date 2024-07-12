from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.options import (
    add_option,
    delete_option,
    retrieve_option,
    retrieve_options,
    update_option,
)
from server.models.options import (
    ErrorResponseModel,
    ResponseModel,
    Options,
    UpdateOptionsModel,
)

router = APIRouter()


@router.post("/", response_description="Option data added into the database")
async def add_option_data(option: Options = Body(...)):
    option = jsonable_encoder(option)
    new_option = await add_option(option)
    return ResponseModel(new_option, "Option added successfully.")


@router.get("/", response_description="Options retrieved")
async def get_options():
    options = await retrieve_options()
    if options:
        return ResponseModel(options, "Options data retrieved successfully")
    return ResponseModel(options, "Empty list returned")


@router.get("/{id}", response_description="Option data retrieved")
async def get_option_data(id):
    option = await retrieve_option(id)
    if option:
        return ResponseModel(option, "Option data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Option doesn't exist.")


@router.put("/{id}")
async def update_option_data(id: str, req: UpdateOptionsModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_option = await update_option(id, req)
    if updated_option:
        return ResponseModel(
            "Option with ID: {} name update is successful".format(id),
            "Option name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Option data.",
    )


@router.delete("/{id}", response_description="Option data deleted from the database")
async def delete_option_data(id: str):
    deleted_option = await delete_option(id)
    if deleted_option:
        return ResponseModel(
            "Plan with ID: {} removed".format(
                id), "Option deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Option with id {0} doesn't exist".format(id)
    )
