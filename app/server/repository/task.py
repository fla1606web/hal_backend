from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config


client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

task_collection = database.get_collection("task")

# helpers


def task_helper(task) -> dict:
    return {
        "name": task["name"],
        "id_entity": task["id_entity"],
        "id_task_type": task["id_task_type"],
        "expression": task["expression"],
        "cron": task["cron"],
        "active": task["active"]
    }


# crud operations
# Retrieve all Task present in the database
async def retrieve_tasks():
    tasks = []
    for task in task_collection.find():
        tasks.append(task_helper(task))
    return tasks


# Add a new Task into to the database
async def add_task(task_data: dict) -> dict:
    task = task_collection.insert_one(task_data)
    new_task = task_collection.find_one({"_id": task.inserted_id})
    return task_helper(new_task)


# Retrieve a Task with a matching ID
async def retrieve_task(id: str) -> dict:
    task = task_collection.find_one({"_id": ObjectId(id)})
    if task:
        return task_helper(task)


# Update a Task with a matching ID
async def update_task(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    task = task_collection.find_one({"_id": ObjectId(id)})
    if task:
        updated_task = task_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_task:
            return True
        return False


# Delete a Task from the database
async def delete_task(id: str):
    task = task_collection.find_one({"_id": ObjectId(id)})
    if task:
        task_collection.delete_one({"_id": ObjectId(id)})
        return True
