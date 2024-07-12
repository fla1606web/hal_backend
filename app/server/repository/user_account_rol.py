from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

user_account_rol_collection = database.get_collection("users_accounts_rols")

# helpers


def user_account_rol_helper(user_account_rol) -> dict:
    return {
        "id_account": str(user_account_rol["id_account"]),
        "name": user_account_rol["name"],
        "active": user_account_rol["active"]
    }


# crud operations
# Retrieve all users_accounts_rols present in the database
async def retrieve_users_accounts_rols():
    users_accounts_rols = []
    for user in user_account_rol_collection.find():
        users_accounts_rols.append(user_account_rol_helper(user))
    return users_accounts_rols


# Add a new user_account_rol into to the database
async def add_user_account_rol(user_account_rol_data: dict) -> dict:
    user_account_rol = user_account_rol_collection.insert_one(
        user_account_rol_data)
    new_user_account_rol = user_account_rol_collection.find_one(
        {"_id": user_account_rol.inserted_id})
    return user_account_rol_helper(new_user_account_rol)


# Retrieve a user_account_rol with a matching ID
async def retrieve_user_account_rol(id: str) -> dict:
    user_account_rol = user_account_rol_collection.find_one(
        {"_id": ObjectId(id)})
    if user_account_rol:
        return user_account_rol_helper(user_account_rol)


# Update a user_account_rol with a matching ID
async def update_user_account_rol(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user_account_rol = user_account_rol_collection.find_one(
        {"_id": ObjectId(id)})
    if user_account_rol:
        updated_user_account_rol = user_account_rol_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user_account_rol:
            return True
        return False


# Delete a user_account_rol from the database
async def delete_user_account_rol(id: str):
    user_account_rol = user_account_rol_collection.find_one(
        {"_id": ObjectId(id)})
    if user_account_rol:
        user_account_rol_collection.delete_one({"_id": ObjectId(id)})
        return True
