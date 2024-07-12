from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

notification_collection = database.get_collection("notifications")

# helpers


def notification_helper(notification) -> dict:
    return {
        "mails_to_notify": notification["mails_to_notify"],
        "phones_to_notify": notification["phones_to_notify"],
        "users_to_notify": notification["users_to_notify"],
        "id_tamplate_mail": notification["id_tamplate_mail"],
        "id_tamplate_whatsapp": notification["id_tamplate_whatsapp"],
        "id_tamplate_push": notification["id_tamplate_push"]
    }


# crud operations
# Retrieve all Notifications present in the database
async def retrieve_notifications():
    notifications = []
    for notification in notification_collection.find():
        notifications.append(notification_helper(notification))
    return notifications


# Add a new Notification into to the database
async def add_notification(notification_data: dict) -> dict:
    notification = notification_collection.insert_one(notification_data)
    new_notification = notification_collection.find_one(
        {"_id": notification.inserted_id})
    return notification_helper(new_notification)


# Retrieve a notification with a matching ID
async def retrieve_notification(id: str) -> dict:
    notification = notification_collection.find_one({"_id": ObjectId(id)})
    if notification:
        return notification_helper(notification)


async def retrieve_notification_object(id: str):
    return notification_collection.find_one({"_id": ObjectId(id)})


# Update a notification with a matching ID
async def update_notification(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    notification = notification_collection.find_one({"_id": ObjectId(id)})
    if notification:
        updated_notification = notification_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_notification:
            return True
        return False


# Delete a notification from the database
async def delete_notification(id: str):
    notification = notification_collection.find_one({"_id": ObjectId(id)})
    if notification:
        notification_collection.delete_one({"_id": ObjectId(id)})
        return True
