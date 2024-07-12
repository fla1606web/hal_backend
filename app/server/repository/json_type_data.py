from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

json_type_data_collection = database.get_collection("json_type_data")

# helpers


def json_type_data_helper(json_type_data) -> dict:
    return {
        "name": json_type_data["name"],
    }


# crud operations
# Retrieve all Json Type Data present in the database
async def retrieve_jsons_type_data():
    jsons_type_data = []
    for json_type_data in json_type_data_collection.find():
        jsons_type_data.append(json_type_data_helper(json_type_data))
    return jsons_type_data


# Add a new Json Type Data into to the database
async def add_json_type_data(json_type_data_data: dict) -> dict:
    json_type_data = json_type_data_collection.insert_one(json_type_data_data)
    new_json_type_data = json_type_data_collection.find_one(
        {"_id": json_type_data.inserted_id})
    return json_type_data_helper(new_json_type_data)


# Retrieve a Json Type Data with a matching ID
async def retrieve_json_type_data(id: str) -> dict:
    json_type_data = json_type_data_collection.find_one({"_id": ObjectId(id)})
    if json_type_data:
        return json_type_data_helper(json_type_data)


async def retrieve_json_type_data_object(id: str):
    return json_type_data_collection.find_one({"_id": ObjectId(id)})


# Update a Json Type Data with a matching ID
async def update_json_type_data(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    json_type_data = json_type_data_collection.find_one({"_id": ObjectId(id)})
    if json_type_data:
        updated_json_type_data = json_type_data_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_json_type_data:
            return True
        return False


# Delete a Json Type Data from the database
async def delete_json_type_data(id: str):
    json_type_data = json_type_data_collection.find_one({"_id": ObjectId(id)})
    if json_type_data:
        json_type_data_collection.delete_one({"_id": ObjectId(id)})
        return True
