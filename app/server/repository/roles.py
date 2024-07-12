from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config


client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

rol_collection = database.get_collection("roles")

# helpers


def rol_helper(rol) -> dict:
    return {
        "id_user": rol["id_user"],
        "view": rol["view"],
        "create": rol["create"],
        "modify": rol["modify"]
    }


# crud operations
# Retrieve all Roles present in the database
async def retrieve_rols():
    rols = []
    for rol in rol_collection.find():
        rols.append(rol_helper(rol))
    return rols


# Add a new Rol into to the database
async def add_rol(rol_data: dict) -> dict:
    rol = rol_collection.insert_one(rol_data)
    new_rol = rol_collection.find_one({"_id": rol.inserted_id})
    return rol_helper(new_rol)


# Retrieve a Rol with a matching ID
async def retrieve_rol(id: str) -> dict:
    rol = rol_collection.find_one({"_id": ObjectId(id)})
    if rol:
        return rol_helper(rol)


# Update a Rol with a matching ID
async def update_rol(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    rol = rol_collection.find_one({"_id": ObjectId(id)})
    if rol:
        updated_rol = rol_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_rol:
            return True
        return False


# Delete a Rol from the database
async def delete_rol(id: str):
    rol = rol_collection.find_one({"_id": ObjectId(id)})
    if rol:
        rol_collection.delete_one({"_id": ObjectId(id)})
        return True
