from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config


client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

entity_workflow_collection = database.get_collection("entity_workflow")

# helpers


def entity_workflow_helper(entity_workflow) -> dict:
    return {
        "id_entity": entity_workflow["id_entity"],
        "id_entity_state_origin": entity_workflow["id_entity_state_origin"],
        "name_action": entity_workflow["name_action"],
        "color": entity_workflow["color"],
        "icon": entity_workflow["icon"],
        "fields": entity_workflow["fields"],
        "roles": entity_workflow["roles"],
        "active": entity_workflow["active"]
    }


# crud operations
# Retrieve all Entitys Workflow present in the database
async def retrieve_entitys_workflow():
    entitys_workflow = []
    for entity_workflow in entity_workflow_collection.find():
        entitys_workflow.append(entity_workflow_helper(entity_workflow))
    return entitys_workflow


# Add a new Entity Workflow into to the database
async def add_entity_workflow(entity_workflow_data: dict) -> dict:
    entity_workflow = entity_workflow_collection.insert_one(
        entity_workflow_data)
    new_entity_workflow = entity_workflow_collection.find_one(
        {"_id": entity_workflow.inserted_id})
    return entity_workflow_helper(new_entity_workflow)


# Retrieve a Entity Workflow with a matching ID
async def retrieve_entity_workflow(id: str) -> dict:
    entity_workflow = entity_workflow_collection.find_one(
        {"_id": ObjectId(id)})
    if entity_workflow:
        return entity_workflow_helper(entity_workflow)


# Update a Entity Workflow with a matching ID
async def update_entity_workflow(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    entity_workflow = entity_workflow_collection.find_one(
        {"_id": ObjectId(id)})
    if entity_workflow:
        updated_entity_workflow = entity_workflow_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_entity_workflow:
            return True
        return False


# Delete a Entity Workflow from the database
async def delete_entity_workflow(id: str):
    entity_workflow = entity_workflow_collection.find_one(
        {"_id": ObjectId(id)})
    if entity_workflow:
        entity_workflow_collection.delete_one({"_id": ObjectId(id)})
        return True
