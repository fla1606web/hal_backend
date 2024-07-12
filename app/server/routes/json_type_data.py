from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.json_type_data import (
    add_json_type_data,
    delete_json_type_data,
    retrieve_json_type_data,
    retrieve_jsons_type_data,
    update_json_type_data,
)
from server.models.json_type_data import (
    ErrorResponseModel,
    ResponseModel,
    JsonTypeData,
    UpdateJsonTypeDataModel,
)

router = APIRouter()


@router.post("/", response_description="Json Type data added into the database")
async def add_json_type_data_data(json_type_data: JsonTypeData = Body(...)):
    json_type_data = jsonable_encoder(json_type_data)
    new_json_type_data = await add_json_type_data(json_type_data)
    return ResponseModel(new_json_type_data, "Json Type Data added successfully.")


@router.get("/", response_description="Json Type Data retrieved")
async def get_jsons_type_data():
    jsons_type_data = await retrieve_jsons_type_data()
    if jsons_type_data:
        return ResponseModel(jsons_type_data, "Json Type data retrieved successfully")
    return ResponseModel(jsons_type_data, "Empty list returned")


@router.get("/{id}", response_description="Json Type data retrieved")
async def get_json_type_data(id):
    json_type_data = await retrieve_json_type_data(id)
    if json_type_data:
        return ResponseModel(json_type_data, "Json Type data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Action type doesn't exist.")


@router.put("/{id}")
async def update_json_type_data_data(id: str, req: UpdateJsonTypeDataModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_json_type_data = await update_json_type_data(id, req)
    if updated_json_type_data:
        return ResponseModel(
            "Json Type Data with ID: {} name update is successful".format(
                id),
            "Json Type Data name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Json Type data.",
    )


@router.delete("/{id}", response_description="Json Type data deleted from the database")
async def delete_json_type_data_data(id: str):
    deleted_json_type_data = await delete_json_type_data(id)
    if deleted_json_type_data:
        return ResponseModel(
            "Json Type Data with ID: {} removed".format(
                id), "Action Type deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Json Type Data with id {0} doesn't exist".format(
            id)
    )
