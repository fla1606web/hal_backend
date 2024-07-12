from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

http_auth_collection = database.get_collection("http_auth")

# helpers


def http_auth_helper(http_auth) -> dict:
    return {
        "name": http_auth["name"],
        "host": http_auth["host"],
        "method": http_auth["method"],
        "id_http_auth_type": http_auth["id_http_auth_type"]
    }


# crud operations
# Retrieve all Http Auth present in the database
async def retrieve_http_auths():
    auths = []
    for http_auth in http_auth_collection.find():
        auths.append(http_auth_helper(http_auth))
    return auths


# Add a new Http Auth into to the database
async def add_http_auth(http_auth_data: dict) -> dict:
    http_auth = http_auth_collection.insert_one(http_auth_data)
    new_http_auth = http_auth_collection.find_one(
        {"_id": http_auth.inserted_id})
    return http_auth_helper(new_http_auth)


# Retrieve a Http Auth with a matching ID
async def retrieve_http_auth(id: str) -> dict:
    http_auth = http_auth_collection.find_one({"_id": ObjectId(id)})
    if http_auth:
        return http_auth_helper(http_auth)


async def retrieve_http_auth_object(id: str):
    return http_auth_collection.find_one({"_id": ObjectId(id)})


# Update a Http Auth with a matching ID
async def update_http_auth(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    http_auth = http_auth_collection.find_one({"_id": ObjectId(id)})
    if http_auth:
        updated_http_auth = http_auth_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_http_auth:
            return True
        return False


# Delete a Http Auth from the database
async def delete_http_auth(id: str):
    http_auth = http_auth_collection.find_one({"_id": ObjectId(id)})
    if http_auth:
        http_auth_collection.delete_one({"_id": ObjectId(id)})
        return True
