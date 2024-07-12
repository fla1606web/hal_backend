from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config


client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

entity_state_collection = database.get_collection("entity_state")

# helpers


def entity_state_helper(entity_state) -> dict:
    return {
        "id_entity": entity_state["id_entity"],
        "name": entity_state["name"],
        "color": entity_state["color"],
        "icon": entity_state["icon"],
        "active": entity_state["active"]
    }


# crud operations
# Retrieve all Entitys State present in the database
async def retrieve_entitys_state():
    entitys_state = []
    for entity_state in entity_state_collection.find():
        entitys_state.append(entity_state_helper(entity_state))
    return entitys_state


# Add a new Entity State into to the database
async def add_entity_state(entity_state_data: dict) -> dict:
    entity_state = entity_state_collection.insert_one(entity_state_data)
    new_entity_state = entity_state_collection.find_one(
        {"_id": entity_state.inserted_id})
    return entity_state_helper(new_entity_state)


# Retrieve a Entity State with a matching ID
async def retrieve_entity_state(id: str) -> dict:
    entity_state = entity_state_collection.find_one({"_id": ObjectId(id)})
    if entity_state:
        return entity_state_helper(entity_state)


# Update a Entity State with a matching ID
async def update_entity_state(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    entity_state = entity_state_collection.find_one({"_id": ObjectId(id)})
    if entity_state:
        updated_entity_state = entity_state_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_entity_state:
            return True
        return False


# Delete a Entity State from the database
async def delete_entity_state(id: str):
    entity_state = entity_state_collection.find_one({"_id": ObjectId(id)})
    if entity_state:
        entity_state_collection.delete_one({"_id": ObjectId(id)})
        return True
