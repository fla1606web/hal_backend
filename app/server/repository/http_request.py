from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

http_request_collection = database.get_collection("http_requests")

# helpers


def http_request_helper(http_request) -> dict:
    return {
        "name": http_request["name"],
        "host": http_request["host"],
        "method": http_request["method"],
        "id_http_auth": http_request["id_http_auth"],
        "header": http_request["header"],
        "query_string": http_request["query_string"],
        "body_type": http_request["body_type"],
        "content_type": http_request["content_type"],
        "request": http_request["request"],
        "response": http_request["response"]
    }


# crud operations
# Retrieve all http_request present in the database
async def retrieve_http_requests():
    requests = []
    for http_request in http_request_collection.find():
        requests.append(http_request_helper(http_request))
    return requests


# Add a new http_request into to the database
async def add_http_request(http_request_data: dict) -> dict:
    http_request = http_request_collection.insert_one(http_request_data)
    new_http_request = http_request_collection.find_one(
        {"_id": http_request.inserted_id})
    return http_request_helper(new_http_request)


# Retrieve a http_request with a matching ID
async def retrieve_http_request(id: str) -> dict:
    http_request = http_request_collection.find_one({"_id": ObjectId(id)})
    if http_request:
        return http_request_helper(http_request)


async def retrieve_http_request_object(id: str):
    return http_request_collection.find_one({"_id": ObjectId(id)})


# Update a http_request with a matching ID
async def update_http_request(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    http_request = http_request_collection.find_one({"_id": ObjectId(id)})
    if http_request:
        updated_http_request = http_request_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_http_request:
            return True
        return False


# Delete a http_request from the database
async def delete_http_request(id: str):
    http_request = http_request_collection.find_one({"_id": ObjectId(id)})
    if http_request:
        http_request_collection.delete_one({"_id": ObjectId(id)})
        return True
