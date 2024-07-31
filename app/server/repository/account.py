from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

account_collection = database.get_collection("accounts")

# helpers
def account_helper(account) -> dict:
    return {
        "id": str(account["_id"]),
        "name": account["name"],
        "id_plan": account["id_plan"],
        "database_host": account["database_host"],
        "database_name": account["database_name"],
        "active": account["active"],
    }


# crud operations
# Retrieve all accounts present in the database
async def retrieve_accounts():
    accounts = []
    for account in account_collection.find():
        accounts.append(account_helper(account))
    return accounts

# Add a new account into to the database
async def add_account(account_data: dict) -> dict:
    account = account_collection.insert_one(account_data)
    new_account = account_collection.find_one({"_id": account.inserted_id})
    return account_helper(new_account)

# Retrieve a account with a matching ID
async def retrieve_account(id: str) -> dict:
    account = account_collection.find_one({"_id": ObjectId(id)})
    if account:
        return account_helper(account)

async def retrieve_account_object(id: str):
    return account_collection.find_one({"_id": ObjectId(id)})

# Update a account with a matching ID
async def update_account(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    account = account_collection.find_one({"_id": ObjectId(id)})
    if account:
        updated_account = account_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_account:
            return True
        return False

# Delete a account from the database
async def delete_account(id: str):
    account = account_collection.find_one({"_id": ObjectId(id)})
    if account:
        account_collection.delete_one({"_id": ObjectId(id)})
        return True
