from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

entity_collection = database.get_collection("entities")

# helpers
def entity_helper(entity) -> dict:
    return {
        "id": str(entity["_id"]),
        "name": entity["name"],
        "id_account": entity["id_account"],
        "collection_name": entity["collection_name"],
        "color": entity["color"],
        "icon": entity["icon"],
        "active": entity["active"],
    }


# crud operations
# Retrieve all entities present in the database
async def retrieve_entities():
    entities = []
    for entity in entity_collection.find():
        entities.append(entity_helper(entity))
    return entities

# crud operations
# Retrieve all entities present in the database
async def retrieve_entities_account(id: str):
    entities = []
    for entity in entity_collection.find({"id_account": id}):
        entities.append(entity_helper(entity))
    return entities


# Add a new entity into to the database
async def add_entity(entity_data: dict) -> dict:
    entity = entity_collection.insert_one(entity_data)
    new_entity = entity_collection.find_one({"_id": entity.inserted_id})
    return entity_helper(new_entity)

# Retrieve a entity with a matching ID
async def retrieve_entity(id: str) -> dict:
    entity = entity_collection.find_one({"_id": ObjectId(id)})
    if entity:
        return entity_helper(entity)
        

# Update a entity with a matching ID
async def update_entity(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    entity = entity_collection.find_one({"_id": ObjectId(id)})
    if entity:
        updated_entity = entity_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_entity:
            return True
        return False

# Delete a entity from the database
async def delete_entity(id: str):
    entity = entity_collection.find_one({"_id": ObjectId(id)})
    if entity:
        entity_collection.delete_one({"_id": ObjectId(id)})
        return True
