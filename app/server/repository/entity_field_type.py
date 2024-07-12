from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config


client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

entity_field_type_collection = database.get_collection("entitys_field_type")

# helpers


def entity_field_type_helper(entity_field_type) -> dict:
    return {
        "name": entity_field_type["name"],
        "active": entity_field_type["active"]
    }


# crud operations
# Retrieve all entitys_field_type present in the database
async def retrieve_entitys_field_type():
    entitys_field_type = []
    for entity_field_type in entity_field_type_collection.find():
        entitys_field_type.append(entity_field_type_helper(entity_field_type))
    return entitys_field_type


# Add a new entity_field_type into to the database
async def add_entity_field_type(entity_field_type_data: dict) -> dict:
    entity_field_type = entity_field_type_collection.insert_one(
        entity_field_type_data)
    new_entity_field_type = entity_field_type_collection.find_one(
        {"_id": entity_field_type.inserted_id})
    return entity_field_type_helper(new_entity_field_type)


# Retrieve a entity_field_type with a matching ID
async def retrieve_entity_field_type(id: str) -> dict:
    entity_field_type = entity_field_type_collection.find_one(
        {"_id": ObjectId(id)})
    if entity_field_type:
        return entity_field_type_helper(entity_field_type)


# Update a entity_field_type with a matching ID
async def update_entity_field_type(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    entity_field_type = entity_field_type_collection.find_one(
        {"_id": ObjectId(id)})
    if entity_field_type:
        updated_entity_field_type = entity_field_type_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_entity_field_type:
            return True
        return False


# Delete a entity_field_type from the database
async def delete_entity_field_type(id: str):
    entity_field_type = entity_field_type_collection.find_one(
        {"_id": ObjectId(id)})
    if entity_field_type:
        entity_field_type_collection.delete_one({"_id": ObjectId(id)})
        return True
