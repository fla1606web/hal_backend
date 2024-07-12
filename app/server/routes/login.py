from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json

from app.server.repository.login import (
    exits_user,
    generate_token,
    verify_token,
    renew_token
)

from server.models.login import (
    ErrorResponseModel,
    ResponseModel,
    Login,
    UpdateLoginModel,
)

router = APIRouter()

@router.post("/")
async def login(login: Login):
    user = await exits_user(login) 
    if user != None:
        #access_token = ResponseModel
        #access_token.code = 200
        #access_token.message = "OK"
        #access_token.data = generate_token(user["id_account"], str(user["_id"]), True, login)
        token = generate_token(user["id_account"], str(user["_id"]), True, login)
        data = {
            "id_account": user["id_account"],
            "token": token
        }
        _data = json.dumps(data)
        return ResponseModel(_data, "OK")
    else:
        return ErrorResponseModel("error", "", "The username or password you have entered is incorrect.")
    
@router.post("/renew")
async def login(token: str):
    token_renew = renew_token(token) 
    if token_renew != "":
        access_token = ResponseModel
        access_token.code = 200
        access_token.message = "OK"
        access_token.data = token_renew
        return access_token
    else:
        return {"status": "error", "message": "The token received is invalid"}