from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.http_request import (
    add_http_request,
    delete_http_request,
    retrieve_http_request,
    retrieve_http_requests,
    update_http_request,
)
from server.models.http_request import (
    ErrorResponseModel,
    ResponseModel,
    HttpRequest,
    UpdateHttpRequestModel,
)

router = APIRouter()


@router.post("/", response_description="Http Request data added into the database")
async def add_http_request_data(http_request: HttpRequest = Body(...)):
    http_request = jsonable_encoder(http_request)
    new_http_request = await add_http_request(http_request)
    return ResponseModel(new_http_request, "Http Request added successfully.")


@router.get("/", response_description="Http Request retrieved")
async def get_http_requests():
    requests = await retrieve_http_requests()
    if requests:
        return ResponseModel(requests, "Http Request data retrieved successfully")
    return ResponseModel(requests, "Empty list returned")


@router.get("/{id}", response_description="Http Request data retrieved")
async def get_http_request_data(id):
    http_request = await retrieve_http_request(id)
    if http_request:
        return ResponseModel(http_request, "Http Request data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Http Request doesn't exist.")


@router.put("/{id}")
async def update_http_request_data(id: str, req: UpdateHttpRequestModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_http_request = await update_http_request(id, req)
    if updated_http_request:
        return ResponseModel(
            "Http Request with ID: {} name update is successful".format(id),
            "Http Request name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Http Request data.",
    )


@router.delete("/{id}", response_description="Http Request data deleted from the database")
async def delete_http_request_data(id: str):
    deleted_http_request = await delete_http_request(id)
    if deleted_http_request:
        return ResponseModel(
            "Http Request with ID: {} removed".format(
                id), "Http Request deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Http Request with id {0} doesn't exist".format(
            id)
    )
