from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

notification_type_collection = database.get_collection("notification_type")

# helpers


def notification_type_helper(notification_type) -> dict:
    return {
        "name": notification_type["name"],
        "active": notification_type["active"]
    }


# crud operations
# Retrieve all Notifications Type present in the database
async def retrieve_notifications_type():
    notifications_type = []
    for notification_type in notification_type_collection.find():
        notifications_type.append(notification_type_helper(notification_type))
    return notifications_type


# Add a new Notification type into to the database
async def add_notification_type(notification_data: dict) -> dict:
    notification_type = notification_type_collection.insert_one(
        notification_data)
    new_notification_type = notification_type_collection.find_one(
        {"_id": notification_type.inserted_id})
    return notification_type_helper(new_notification_type)


# Retrieve a Notification Type with a matching ID
async def retrieve_notification_type(id: str) -> dict:
    notification_type = notification_type_collection.find_one(
        {"_id": ObjectId(id)})
    if notification_type:
        return notification_type_helper(notification_type)


async def retrieve_notification_type_object(id: str):
    return notification_type_collection.find_one({"_id": ObjectId(id)})


# Update a Notification Type with a matching ID
async def update_notification_type(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    notification_type = notification_type_collection.find_one(
        {"_id": ObjectId(id)})
    if notification_type:
        updated_notification_type = notification_type_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_notification_type:
            return True
        return False


# Delete a Notification Type from the database
async def delete_notification_type(id: str):
    notification_type = notification_type_collection.find_one(
        {"_id": ObjectId(id)})
    if notification_type:
        notification_type_collection.delete_one({"_id": ObjectId(id)})
        return True
