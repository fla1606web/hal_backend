from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.json import (
    add_json,
    delete_json,
    retrieve_json,
    retrieve_jsons,
    update_json,
)
from server.models.json import (
    ErrorResponseModel,
    ResponseModel,
    Json,
    UpdateJsonModel,
)

router = APIRouter()


@router.post("/", response_description="Json data added into the database")
async def add_action_data(json: Json = Body(...)):
    json = jsonable_encoder(json)
    new_json = await add_json(json)
    return ResponseModel(new_json, "Json added successfully.")


@router.get("/", response_description="Json retrieved")
async def get_jsons():
    jsons = await retrieve_jsons()
    if jsons:
        return ResponseModel(jsons, "Json data retrieved successfully")
    return ResponseModel(jsons, "Empty list returned")


@router.get("/{id}", response_description="Json data retrieved")
async def get_action_data(id):
    json = await retrieve_json(id)
    if json:
        return ResponseModel(json, "Json data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Json doesn't exist.")


@router.put("/{id}")
async def update_action_data(id: str, req: UpdateJsonModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_json = await update_json(id, req)
    if updated_json:
        return ResponseModel(
            "Json with ID: {} name update is successful".format(id),
            "Json name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Json data.",
    )


@router.delete("/{id}", response_description="Json data deleted from the database")
async def delete_json_data(id: str):
    deleted_json = await delete_json(id)
    if deleted_json:
        return ResponseModel(
            "Json with ID: {} removed".format(
                id), "Json deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Json with id {0} doesn't exist".format(
            id)
    )
