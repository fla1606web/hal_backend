from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

json_collection = database.get_collection("json")

# helpers


def json_helper(json) -> dict:
    return {
        "name": json["name"],
        "data": json["data"]
    }


# crud operations
# Retrieve all Json present in the database
async def retrieve_jsons():
    jsons = []
    for json in json_collection.find():
        jsons.append(json_helper(json))
    return jsons


# Add a new Json into to the database
async def add_json(json_data: dict) -> dict:
    json = json_collection.insert_one(json_data)
    new_json = json_collection.find_one({"_id": json.inserted_id})
    return json_helper(new_json)


# Retrieve a Json with a matching ID
async def retrieve_json(id: str) -> dict:
    json = json_collection.find_one({"_id": ObjectId(id)})
    if json:
        return json_helper(json)


async def retrieve_json_object(id: str):
    return json_collection.find_one({"_id": ObjectId(id)})


# Update a Json with a matching ID
async def update_json(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    json = json_collection.find_one({"_id": ObjectId(id)})
    if json:
        updated_json = json_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_json:
            return True
        return False


# Delete a Json from the database
async def delete_json(id: str):
    json = json_collection.find_one({"_id": ObjectId(id)})
    if json:
        json_collection.delete_one({"_id": ObjectId(id)})
        return True
