from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config


client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

task_type_collection = database.get_collection("task_type")

# helpers


def task_type_helper(task_type) -> dict:
    return {
        "name": task_type["name"],
        "active": task_type["active"]
    }


# crud operations
# Retrieve all Task Type present in the database
async def retrieve_tasks_type():
    tasks_type = []
    for task_type in task_type_collection.find():
        tasks_type.append(task_type_helper(task_type))
    return tasks_type


# Add a new Task Type into to the database
async def add_task_type(task_type_data: dict) -> dict:
    task_type = task_type_collection.insert_one(task_type_data)
    new_task_type = task_type_collection.find_one(
        {"_id": task_type.inserted_id})
    return task_type_helper(new_task_type)


# Retrieve a Task Type with a matching ID
async def retrieve_task_type(id: str) -> dict:
    task_type = task_type_collection.find_one({"_id": ObjectId(id)})
    if task_type:
        return task_type_helper(task_type)


# Update a Task Type with a matching ID
async def update_task_type(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    task_type = task_type_collection.find_one({"_id": ObjectId(id)})
    if task_type:
        updated_task_type = task_type_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_task_type:
            return True
        return False


# Delete a Task Type from the database
async def delete_task_type(id: str):
    task_type = task_type_collection.find_one({"_id": ObjectId(id)})
    if task_type:
        task_type_collection.delete_one({"_id": ObjectId(id)})
        return True
