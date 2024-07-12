from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.roles import (
    add_rol,
    delete_rol,
    retrieve_rol,
    retrieve_rols,
    update_rol,
)
from server.models.roles import (
    ErrorResponseModel,
    ResponseModel,
    Roles,
    UpdateRolesModel,
)

router = APIRouter()


@router.post("/", response_description="Rol data added into the database")
async def add_rol_data(rol: Roles = Body(...)):
    rol = jsonable_encoder(rol)
    new_rol = await add_rol(rol)
    return ResponseModel(new_rol, "Rol added successfully.")


@router.get("/", response_description="Rols retrieved")
async def get_rols():
    rols = await retrieve_rols()
    if rols:
        return ResponseModel(rols, "Rols data retrieved successfully")
    return ResponseModel(rols, "Empty list returned")


@router.get("/{id}", response_description="Rol data retrieved")
async def get_rol_data(id):
    rol = await retrieve_rol(id)
    if rol:
        return ResponseModel(rol, "Rol data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Rol doesn't exist.")


@router.put("/{id}")
async def update_rol_data(id: str, req: UpdateRolesModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_rol = await update_rol(id, req)
    if updated_rol:
        return ResponseModel(
            "Rol with ID: {} name update is successful".format(id),
            "Rol name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Rol data.",
    )


@router.delete("/{id}", response_description="Rol data deleted from the database")
async def delete_rol_data(id: str):
    deleted_rol = await delete_rol(id)
    if deleted_rol:
        return ResponseModel(
            "Rol with ID: {} removed".format(id), "Rol deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Rol with id {0} doesn't exist".format(id)
    )
