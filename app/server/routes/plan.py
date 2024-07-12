from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.repository.plan import (
    add_plan,
    delete_plan,
    retrieve_plan,
    retrieve_plans,
    update_plan,
)
from server.models.plan import (
    ErrorResponseModel,
    ResponseModel,
    Plan,
    UpdatePlanModel,
)

router = APIRouter()


@router.post("/", response_description="Plan data added into the database")
async def add_plan_data(plan: Plan = Body(...)):
    plan = jsonable_encoder(plan)
    new_plan = await add_plan(plan)
    return ResponseModel(new_plan, "Plan added successfully.")


@router.get("/", response_description="Plans retrieved")
async def get_plans():
    plans = await retrieve_plans()
    if plans:
        return ResponseModel(plans, "Plans data retrieved successfully")
    return ResponseModel(plans, "Empty list returned")


@router.get("/{id}", response_description="Plan data retrieved")
async def get_plan_data(id):
    plan = await retrieve_plan(id)
    if plan:
        return ResponseModel(plan, "Plan data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Plan doesn't exist.")


@router.put("/{id}")
async def update_plan_data(id: str, req: UpdatePlanModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_plan = await update_plan(id, req)
    if updated_plan:
        return ResponseModel(
            "Plan with ID: {} name update is successful".format(id),
            "Plan name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Plan data.",
    )


@router.delete("/{id}", response_description="Plan data deleted from the database")
async def delete_plan_data(id: str):
    deleted_plan = await delete_plan(id)
    if deleted_plan:
        return ResponseModel(
            "Plan with ID: {} removed".format(id), "Plan deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Plan with id {0} doesn't exist".format(id)
    )
