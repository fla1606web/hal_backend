from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

action_type_collection = database.get_collection("action_type")

# helpers


def action_type_helper(action_type) -> dict:
    return {
        "name": action_type["name"],
        "active": action_type["active"]
    }


# crud operations
# Retrieve all Action Type present in the database
async def retrieve_actions_type():
    actions_type = []
    for action_type in action_type_collection.find():
        actions_type.append(action_type_helper(action_type))
    return actions_type


# Add a new Action type into to the database
async def add_action_type(action_type_data: dict) -> dict:
    action_type = action_type_collection.insert_one(
        action_type_data)
    new_action_type = action_type_collection.find_one(
        {"_id": action_type.inserted_id})
    return action_type_helper(new_action_type)


# Retrieve a Action Type with a matching ID
async def retrieve_action_type(id: str) -> dict:
    action_type = action_type_collection.find_one(
        {"_id": ObjectId(id)})
    if action_type:
        return action_type_helper(action_type)


async def retrieve_action_type_object(id: str):
    return action_type_collection.find_one({"_id": ObjectId(id)})


# Update a Action Type with a matching ID
async def update_action_type(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    action_type = action_type_collection.find_one(
        {"_id": ObjectId(id)})
    if action_type:
        updated_action_type = action_type_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_action_type:
            return True
        return False


# Delete a Action Type from the database
async def delete_action_type(id: str):
    action_type = action_type_collection.find_one(
        {"_id": ObjectId(id)})
    if action_type:
        action_type_collection.delete_one({"_id": ObjectId(id)})
        return True
