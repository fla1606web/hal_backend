from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

user_collection = database.get_collection("users")

# helpers
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "id_account": user["id_account"],
        "id_user_account_rol": "",
        "user": user["user"],
        "password": user["password"],
        "mail": user["mail"],
        "name": user["name"],
        "last_name": user["last_name"],
        "telephone": user["telephone"],
        "lang": user["lang"],
        "time_zone": user["time_zone"],
        "token_firebase": user["token_firebase"],
        "active": user["active"],
    }

# crud operations
# Retrieve all users present in the database
async def retrieve_users():
    users = []
    for user in user_collection.find():
        users.append(user_helper(user))
    return users

# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

# Update a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False

# Delete a user from the database
async def delete_user(id: str):
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.delete_one({"_id": ObjectId(id)})
        return True
