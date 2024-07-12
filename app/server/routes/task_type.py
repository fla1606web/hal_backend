from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.task_type import (
    add_task_type,
    delete_task_type,
    retrieve_task_type,
    retrieve_tasks_type,
    update_task_type,
)

from server.models.task_type import (
    ErrorResponseModel,
    ResponseModel,
    TaskType,
    UpdateTaskTypeModel,
)

router = APIRouter()


@router.post("/", response_description="Task Type data added into the database")
async def add_task_type_data(task_type: TaskType = Body(...)):
    task_type = jsonable_encoder(task_type)
    new_task_type = await add_task_type(task_type)
    return ResponseModel(new_task_type, "Task Type added successfully.")


@router.get("/", response_description="Task Type retrieved")
async def get_tasks_type():
    tasks_type = await retrieve_tasks_type()
    if tasks_type:
        return ResponseModel(tasks_type, "Task Type data retrieved successfully")
    return ResponseModel(tasks_type, "Empty list returned")


@router.get("/{id}", response_description="Task Type data retrieved")
async def get_task_type_data(id):
    task_type = await retrieve_task_type(id)
    if task_type:
        return ResponseModel(task_type, "Task Type data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Task Type doesn't exist.")


@router.put("/{id}")
async def update_task_type_data(id: str, req: UpdateTaskTypeModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_task_type = await update_task_type(id, req)
    if updated_task_type:
        return ResponseModel(
            "Task Type with ID: {} name update is successful".format(id),
            "Task Type name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Task Type data.",
    )


@router.delete("/{id}", response_description="Task Type data deleted from the database")
async def delete_task_type_data(id: str):
    deleted_task_type = await delete_task_type(id)
    if deleted_task_type:
        return ResponseModel(
            "Task Type with ID: {} removed".format(
                id), "Task Type deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Task Type with id {0} doesn't exist".format(
            id)
    )
