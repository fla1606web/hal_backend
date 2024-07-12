from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

rols_collection = database.get_collection("roles")

# helpers
def roles_helper(roles) -> dict:
    return {
        "id_rol": str(roles["id_rol"]),
        "id_user": roles["id_user"],
        "view": str(roles["view"]),
        "create": str(roles["create"]),
        "modify": str(roles["modify"])
    }


# crud operations
# Retrieve all rolesa present in the database
async def retrieve_rols():
    rols = []
    for rols_data in rols_collection.find():
        rols.append(roles_helper(rols_data))
    return rols


# Add a new roles into to the database
async def add_rols(rols_data: dict) -> dict:
    rols = rols_collection.insert_one(rols_data)
    new_rols = rols_collection.find_one({"_id": rols.inserted_id})
    return roles_helper(new_rols)


# Retrieve a roles with a matching ID
async def retrieve_rols(id: str) -> dict:
    rols = rols_collection.find_one({"_id": ObjectId(id)})
    if rols:
        return roles_helper(rols)


# Update a roles with a matching ID
async def update_rols(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    rols = rols_collection.find_one({"_id": ObjectId(id)})
    if rols:
        updated_rols = rols_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_rols:
            return True
        return False


# Delete a roles from the database
async def delete_rols(id: str):
    rols = rols_collection.find_one({"_id": ObjectId(id)})
    if rols:
        rols_collection.delete_one({"_id": ObjectId(id)})
        return True
