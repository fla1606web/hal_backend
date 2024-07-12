import gzip
import logging
import sys
import time
from fastapi.responses import JSONResponse

from decouple import config

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import iterate_in_threadpool

from app.server.helper.custom_formatter import CustomFormatter

from server.routes.login import router as LoginRouter
from server.routes.account import router as AccountRouter
from server.routes.user import router as UserRouter
from server.routes.entity import router as EntityRouter
from server.routes.entity_field import router as EntityFieldRouter
from server.routes.data import router as DataRouter
from server.routes.plan import router as PlanRouter
from server.routes.user_account_rol import router as UserAccountRolRouter
from server.routes.entity_field_type import router as EntityFieldTypeRouter
from server.routes.roles import router as RolesRouter
from server.routes.entity_state import router as EntityStateRouter
from server.routes.task import router as TaskRouter
from server.routes.task_type import router as TaskTypeRouter
from server.routes.entity_workflow import router as EntityWorkflowRouter
from server.routes.action import router as ActionRouter
from server.routes.http_request import router as HttpRequestRouter
from server.routes.notifications import router as NotificationsRouter
from server.routes.template import router as TemplateRouter
from server.routes.notification_type import router as NotificationTypeRouter
from server.routes.action_type import router as ActionTypeRouter
from server.routes.options import router as OptionsRouter
from server.routes.json import router as JsonRouter
from server.routes.json_type_data import router as JsonTypeDataRouter
from server.routes.http_auth import router as HttpAuthRouter

from app.server.repository.login import (
    verify_token,
)

from app.server.models.login import (
    ResponseModel, 
    ErrorResponseModel,
)

debug = bool(config("app.debug"))

app = FastAPI()

app.include_router(LoginRouter, tags=["Login"], prefix="/login")
app.include_router(AccountRouter, tags=["Account"], prefix="/account")
app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(EntityRouter, tags=["Entity"], prefix="/entity")
app.include_router(EntityFieldRouter,
                   tags=["EntityField"], prefix="/entityField")
app.include_router(DataRouter, tags=["Data"], prefix="/data")
app.include_router(PlanRouter, tags=["Plan"], prefix="/plan")
app.include_router(UserAccountRolRouter, tags=[
                   "User Account Rol"], prefix="/useraccountrol")
app.include_router(EntityFieldTypeRouter, tags=[
                   "Entity Field Type"], prefix="/entityfieldtype")
app.include_router(RolesRouter, tags=[
                   "Roles"], prefix="/roles")
app.include_router(EntityStateRouter, tags=[
                   "Entity State"], prefix="/entitystate")
app.include_router(TaskRouter, tags=[
                   "Task"], prefix="/task")
app.include_router(TaskTypeRouter, tags=[
                   "Task Type"], prefix="/tasktype")
app.include_router(EntityWorkflowRouter, tags=[
                   "Entity Workflow"], prefix="/entityworkflow")
app.include_router(ActionRouter, tags=[
                   "Action"], prefix="/action")
app.include_router(HttpRequestRouter, tags=[
                   "Http Request"], prefix="/httprequest")
app.include_router(NotificationsRouter, tags=[
                   "Notifications"], prefix="/notifications")
app.include_router(TemplateRouter, tags=[
                   "Templates"], prefix="/templates")
app.include_router(NotificationTypeRouter, tags=[
                   "Notification Type"], prefix="/notificationtype")
app.include_router(ActionTypeRouter, tags=[
                   "Action Type"], prefix="/actiontype")
app.include_router(OptionsRouter, tags=[
                   "Options"], prefix="/options")
app.include_router(JsonRouter, tags=[
                   "Json"], prefix="/json")
app.include_router(JsonTypeDataRouter, tags=[
                   "Json Type Data"], prefix="/jsontypedata")
app.include_router(HttpAuthRouter, tags=[
                   "Http Auth"], prefix="/httpauth")

# Logger
app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
file_format = "%(asctime)s - %(name)s (%(lineno)s) - %(levelname)s - %(threadName)s - %(message)s"
log_formatter = stream_handler.setFormatter(CustomFormatter(file_format))
app.logger.addHandler(stream_handler)

app.logger.info('HAL is starting up')

# Compresion de datos
# app.add_middleware(GZipMiddleware, minimum_size=250)

# CORS
origins = [
    "chrome-extension://*",
    "http://localhost:*",
]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    #allow_origin_regex="chrome-extension://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):

    if ("docs" in request.url.path or "openapi" in request.url.path or "login" in request.url.path or "account" in request.url.path or "user" in request.url.path):
        return await call_next(request)
    
    start_time = time.time()
    
    print(debug)
    print("El request")
    print(request.url.path)

    if debug:
        app.logger.info("Request %s %s q=%s" % (request.method, request.url.path, request.query_params))
    #has_access = verify_token(request.headers)
    has_access = True
    if has_access == True:      
        print("por ejecutar endpoint") 
        response = await call_next(request)
        if debug:
                response_body = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
                # responseData = gzip.decompress(response_body[0])
                #responseData = response_body[0].decode()
                #app.logger.info("Response %s", responseData)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response
    else:
         response_login = ResponseModel
         response_login.code = 401
         response_login.message = "The token is invalid or has expired."
         return JSONResponse(content={
              "message":"The token is invalid or has expired."
            }, status_code=401) 
    