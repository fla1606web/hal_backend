from typing import Any
from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from pydantic import Json
from decouple import config

from app.server.core.model.page_parameters import PageParameters
from app.server.repository.account import retrieve_account_object
from app.server.repository.data import (
    add_data,
    delete_data,
    retrieve_data,
    retrieve_data_id,
    update_data,
)
from server.models.data import (
    ErrorResponseModel,
    ResponseModel,
)
from app.server.core.model.filter import (
    Filter,
)

router = APIRouter()

debug = bool(config("app.debug"))

@router.post("/{account_id}/{entity_name}/", response_description="Data added into the database")
async def add(account_id : str, entity_name : str, data: Json[Any] = Body(...)):
    account = await retrieve_account_object(account_id)
    if account:    
        data = jsonable_encoder(data)
        new_data = await add_data(account, entity_name, data)
        return ResponseModel(new_data, "Entity added successfully.")
    else: 
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error processing your request.",
        )


@router.get("/{account_id}/{entity_name}/", response_description="Data retrieved")
async def get(account_id : str, entity_name: str, request: Request):
    account = await retrieve_account_object(account_id)
    if account:
        app = request.app

        if debug:
            app.logger.info("Account = %s", account)
        
        filters = []
        for k in request.query_params.keys():
            filters.append(Filter(k, request.query_params[k]))
            if debug:
                app.logger.info("%s = %s" % (k, request.query_params[k]))

        fields = []
        print("fields")
        print(fields)
        #fields.append("codigo")
        #fields.append("")
        pageParameters = PageParameters(filters, None, 1, 10, "codigo", "desc", fields)

        data = await retrieve_data(request, account, entity_name, pageParameters)
        if data:
            return ResponseModel(data, "Data retrieved successfully")

        return ResponseModel(data, "Empty list returned")
    else: 
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error processing your request.",
        )

@router.get("/{account_id}/{entity_name}/{id}", response_description="Data retrieved")
async def get(account_id : str, entity_name: str, id):
    account = await retrieve_account_object(account_id)
    if account:    
        data = await retrieve_data_id(account, entity_name, id)
        if data:
            return ResponseModel(data, "Data retrieved successfully")
        return ErrorResponseModel("An error occurred.", 404, "Entity doesn't exist.")
    else: 
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error processing your request.",
        )

@router.put("/{account_id}/{entity_name}/{id}")
async def update(account_id : str, entity_name: str, id: str, req: Json[Any] = Body(...)):
    account = await retrieve_account_object(account_id)
    if account:    
        # req = {k: v for k, v in req.dict().items() if v is not None}
        updated_data = await update_data(account, entity_name, id, req)
        if updated_data:
            return ResponseModel(
                "Entity with ID: {} name update is successful".format(id),
                "Entity name updated successfully",
            )
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error updating the data data.",
        )
    else: 
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error processing your request.",
        )

@router.delete("/{account_id}/{entity_name}/{id}", response_description="Data deleted from the database")
async def delete(account_id : str, entity_name: str, id: str):
    account = await retrieve_account_object(account_id)
    if account:    
        deleted_data = await delete_data(account, entity_name, id)
        if deleted_data:
            return ResponseModel(
                "Entity with ID: {} removed".format(id), "Entity deleted successfully"
            )
        return ErrorResponseModel(
            "An error occurred", 404, "Entity with id {0} doesn't exist".format(id)
        )
    else: 
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error processing your request.",
        )
