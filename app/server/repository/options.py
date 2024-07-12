from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

option_collection = database.get_collection("options")

# helpers


def options_helper(options) -> dict:
    return {
        "name": options["name"],
    }


# crud operations
# Retrieve all Options present in the database
async def retrieve_options():
    options = []
    for option in option_collection.find():
        options.append(options_helper(option))
    return options


# Add a new Option type into to the database
async def add_option(option_data: dict) -> dict:
    option = option_collection.insert_one(
        option_data)
    new_option = option_collection.find_one(
        {"_id": option.inserted_id})
    return options_helper(new_option)


# Retrieve a Option with a matching ID
async def retrieve_option(id: str) -> dict:
    option = option_collection.find_one(
        {"_id": ObjectId(id)})
    if option:
        return options_helper(option)


async def retrieve_option_object(id: str):
    return option_collection.find_one({"_id": ObjectId(id)})


# Update a Option with a matching ID
async def update_option(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    option = option_collection.find_one(
        {"_id": ObjectId(id)})
    if option:
        updated_option = option_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_option:
            return True
        return False


# Delete a Option from the database
async def delete_option(id: str):
    option = option_collection.find_one(
        {"_id": ObjectId(id)})
    if option:
        option_collection.delete_one({"_id": ObjectId(id)})
        return True
