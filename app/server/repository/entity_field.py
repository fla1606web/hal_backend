from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

entity_field_collection = database.get_collection("entity_fields")

# helpers


def entity_field_helper(entity_field) -> dict:
    return {
        "id_entity": entity_field["id_entity"],
        "name": entity_field["name"],
        "field_name": entity_field["field_name"],
        "id_entity_field_type": entity_field["id_entity_field_type"],
        "id_entity_relation": entity_field["id_entity_relation"],
        "required": entity_field["required"],
        "order": entity_field["order"],
        "minimun": entity_field["minimun"],
        "maximun": entity_field["maximun"],
        "options": entity_field["options"],
        "roles": entity_field["roles"],
        "active": entity_field["active"],
    }

# crud operations
# Retrieve all entity_fields present in the database


async def retrieve_entity_fields():
    entity_fields = []
    for entity_field in entity_field_collection.find():
        entity_fields.append(entity_field_helper(entity_field))
    return entity_fields

# Add a new entity_field into to the database


async def add_entity_field(entity_field_data: dict) -> dict:
    entity_field = entity_field_collection.insert_one(entity_field_data)
    new_entity_field = entity_field_collection.find_one(
        {"_id": entity_field.inserted_id})
    return entity_field_helper(new_entity_field)

# Retrieve a entity_field with a matching ID


async def retrieve_entity_field(id: str) -> dict:
    entity_field = entity_field_collection.find_one({"_id": ObjectId(id)})
    if entity_field:
        return entity_field_helper(entity_field)

# Update a entity_field with a matching ID


async def update_entity_field(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    entity_field = entity_field_collection.find_one({"_id": ObjectId(id)})
    if entity_field:
        updated_entity_field = entity_field_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_entity_field:
            return True
        return False

# Delete a entity_field from the database


async def delete_entity_field(id: str):
    entity_field = entity_field_collection.find_one({"_id": ObjectId(id)})
    if entity_field:
        await entity_field_collection.delete_one({"_id": ObjectId(id)})
        return True


# Retrieve all entity_fields present in the database
async def retrieve_entity_fields_id_entity(idEntity: str):
    entity_fields = []
    for entity_field in entity_field_collection.find({"id_entity": idEntity}):
        entity_fields.append(entity_field_helper(entity_field))
    return entity_fields