from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config


client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

plan_collection = database.get_collection("plans")

# helpers


def plan_helper(plan) -> dict:
    return {
        "name": plan["name"],
        "active": plan["active"]
    }


# crud operations
# Retrieve all Plans present in the database
async def retrieve_plans():
    plans = []
    for plan in plan_collection.find():
        plans.append(plan_helper(plan))
    return plans


# Add a new Plan into to the database
async def add_plan(plan_data: dict) -> dict:
    plan = plan_collection.insert_one(plan_data)
    new_plan = plan_collection.find_one({"_id": plan.inserted_id})
    return plan_helper(new_plan)


# Retrieve a Plan with a matching ID
async def retrieve_plan(id: str) -> dict:
    plan = plan_collection.find_one({"_id": ObjectId(id)})
    if plan:
        return plan_helper(plan)


# Update a Plan with a matching ID
async def update_plan(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    plan = plan_collection.find_one({"_id": ObjectId(id)})
    if plan:
        updated_plan = plan_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_plan:
            return True
        return False


# Delete a Plan from the database
async def delete_plan(id: str):
    plan = plan_collection.find_one({"_id": ObjectId(id)})
    if plan:
        plan_collection.delete_one({"_id": ObjectId(id)})
        return True
