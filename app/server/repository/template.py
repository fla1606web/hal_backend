from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

template_collection = database.get_collection("templates")

# helpers


def template_helper(template) -> dict:
    return {
        "name": template["name"],
        "id_template_type": template["id_template_type"],
        "template": template["template"],
        "active": template["active"]
    }


# crud operations
# Retrieve all Templates present in the database
async def retrieve_templates():
    templates = []
    for template in template_collection.find():
        templates.append(template_helper(template))
    return templates


# Add a new Template into to the database
async def add_template(template_data: dict) -> dict:
    template = template_collection.insert_one(template_data)
    new_template = template_collection.find_one({"_id": template.inserted_id})
    return template_helper(new_template)


# Retrieve a Template with a matching ID
async def retrieve_template(id: str) -> dict:
    template = template_collection.find_one({"_id": ObjectId(id)})
    if template:
        return template_helper(template)


async def retrieve_template_object(id: str):
    return template_collection.find_one({"_id": ObjectId(id)})


# Update a Template with a matching ID
async def update_template(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    template = template_collection.find_one({"_id": ObjectId(id)})
    if template:
        updated_template = template_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_template:
            return True
        return False


# Delete a Template from the database
async def delete_template(id: str):
    template = template_collection.find_one({"_id": ObjectId(id)})
    if template:
        template_collection.delete_one({"_id": ObjectId(id)})
        return True
