from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

action_collection = database.get_collection("action")

# helpers


def action_helper(action) -> dict:
    return {
        "name": action["name"],
        "id_task": action["id_task"],
        "id_action_type": action["id_action_type"],
        "id_entity": action["id_entity"],
        "fields": action["fields"],
        "notifications": action["notifications"],
        "id_http_request": action["id_http_request"],
        "script": action["script"],
        "id_action_next": action["id_action_next"],
        "active": action["active"]
    }


# crud operations
# Retrieve all Actions present in the database
async def retrieve_actions():
    actions = []
    for action in action_collection.find():
        actions.append(action_helper(action))
    return actions


# Add a new Action into to the database
async def add_action(action_data: dict) -> dict:
    action = action_collection.insert_one(action_data)
    new_action = action_collection.find_one({"_id": action.inserted_id})
    return action_helper(new_action)


# Retrieve a Action with a matching ID
async def retrieve_action(id: str) -> dict:
    action = action_collection.find_one({"_id": ObjectId(id)})
    if action:
        return action_helper(action)


async def retrieve_action_object(id: str):
    return action_collection.find_one({"_id": ObjectId(id)})


# Update a Action with a matching ID
async def update_action(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    action = action_collection.find_one({"_id": ObjectId(id)})
    if action:
        updated_action = action_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_action:
            return True
        return False


# Delete a Action from the database
async def delete_action(id: str):
    action = action_collection.find_one({"_id": ObjectId(id)})
    if action:
        action_collection.delete_one({"_id": ObjectId(id)})
        return True
