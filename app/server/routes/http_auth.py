from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.http_auth import (
    add_http_auth,
    delete_http_auth,
    retrieve_http_auth,
    retrieve_http_auths,
    update_http_auth,
)
from server.models.http_auth import (
    ErrorResponseModel,
    ResponseModel,
    HttpAuth,
    UpdateHttpAuthModel,
)

router = APIRouter()


@router.post("/", response_description="Http Auth data added into the database")
async def add_http_request_data(http_auth: HttpAuth = Body(...)):
    http_auth = jsonable_encoder(http_auth)
    new_http_auth = await add_http_auth(http_auth)
    return ResponseModel(new_http_auth, "Http Auth added successfully.")


@router.get("/", response_description="Http Auth retrieved")
async def get_http_auths():
    auths = await retrieve_http_auths()
    if auths:
        return ResponseModel(auths, "Http Auth data retrieved successfully")
    return ResponseModel(auths, "Empty list returned")


@router.get("/{id}", response_description="Http Auth data retrieved")
async def get_http_auth_data(id):
    http_auth = await retrieve_http_auth(id)
    if http_auth:
        return ResponseModel(http_auth, "Http Auth data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Http Request doesn't exist.")


@router.put("/{id}")
async def update_http_auth_data(id: str, req: UpdateHttpAuthModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_http_auth = await update_http_auth(id, req)
    if updated_http_auth:
        return ResponseModel(
            "Http Auth with ID: {} name update is successful".format(id),
            "Http Auth name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Http Auth data.",
    )


@router.delete("/{id}", response_description="Http Auth data deleted from the database")
async def delete_http_auth_data(id: str):
    deleted_http_auth = await delete_http_auth(id)
    if deleted_http_auth:
        return ResponseModel(
            "Http Auth with ID: {} removed".format(
                id), "Http Request deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Http Auth with id {0} doesn't exist".format(
            id)
    )
