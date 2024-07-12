from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.user_account_rol import (
    add_user_account_rol,
    delete_user_account_rol,
    retrieve_user_account_rol,
    retrieve_users_accounts_rols,
    update_user_account_rol,
)
from server.models.user_account_rol import (
    ErrorResponseModel,
    ResponseModel,
    UserAccountRol,
    UpdateUserAccountRol,
)

router = APIRouter()


@router.post("/", response_description="user_account_rol data added into the database")
async def add_user_account_rol_data(user_account_rol: UserAccountRol = Body(...)):
    user_account_rol = jsonable_encoder(user_account_rol)
    new_user_account_rol = await add_user_account_rol(user_account_rol)
    return ResponseModel(new_user_account_rol, "user_account_rol added successfully.")


@router.get("/", response_description="users_accounts_rols retrieved")
async def get_users_accounts_rols():
    users_accounts_rols = await retrieve_users_accounts_rols()
    if users_accounts_rols:
        return ResponseModel(users_accounts_rols, "Users_Accounts_Rols data retrieved successfully")
    return ResponseModel(users_accounts_rols, "Empty list returned")


@router.get("/{id}", response_description="users_accounts_rols data retrieved")
async def get_user_account_rol_data(id):
    user_account_rol = await retrieve_user_account_rol(id)
    if user_account_rol:
        return ResponseModel(user_account_rol, "User Account Rol data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.put("/{id}")
async def update_user_account_rol_data(id: str, req: UpdateUserAccountRol = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user_account_rol = await update_user_account_rol(id, req)
    if updated_user_account_rol:
        return ResponseModel(
            "User Account Rol with ID: {} name update is successful".format(
                id),
            "User Account Rol name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/{id}", response_description="User Account Rol data deleted from the database")
async def delete_user_account_rol_data(id: str):
    deleted_user_account_rol = await delete_user_account_rol(id)
    if deleted_user_account_rol:
        return ResponseModel(
            "User Account Rol with ID: {} removed".format(
                id), "User Account Rol deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User Account Rol with id {0} doesn't exist".format(
            id)
    )
