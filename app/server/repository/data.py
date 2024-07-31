from fastapi import Request
from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

from app.server.core.model.page_parameters import PageParameters
from app.server.models.account import Account

debug = bool(config("app.debug"))

def get_collection(account: Account, entity_name: str):
    host = "mongodb://" + account["database_host"] + ":27017/"
    client = MongoClient(host)
    database = client[account["database_name"]]
    return database[entity_name]

async def retrieve_data(request: Request, account: Account, entity_name: str, pageParameters: PageParameters) -> dict:
    data = []

    if debug:
        request.app.logger.info("pageParameters %s", pageParameters.__dict__)

    skip = 0
    if pageParameters.page > 1:
        skip = pageParameters.page-1*pageParameters.pageSize

    pipeline = [
        { "$limit": skip + pageParameters.pageSize },
        { "$skip": skip }
    ]

    if pageParameters.entitySort:
        pipeline.append({ "$sort": { pageParameters.entitySort: pageParameters.entitySortType } })

    if pageParameters.filters:
        filters = []
        for filter in pageParameters.filters:
            filters.append({ filter.name: filter.value })
            print("%s = %s" % (filter.name, filter.value))

        if len(filters)>1:
            pipeline.append({ "$match": { "$and": filters } }) 
        else:
            pipeline.append({ "$match": { filter.name: filter.value } }) 

    if pageParameters.fields:
        projectFields = {}
        for field in pageParameters.fields:
            projectFields[field] = 1
        pipeline.append( { "$project": projectFields })
    
    if debug:
        request.app.logger.info("pipeline %s", pipeline)

    results = get_collection(account, entity_name).aggregate(pipeline)
    for dataRow in results:
        data.append(dataRow)

    return data

# Add a new data into to the database
async def add_data(account: Account, entity_name: str, data: dict) -> dict:
    print("estoy en add repository")
    print(account)
    print(entity_name)
    print(data)
    data = get_collection(account, entity_name).insert_one(data)
    print("inserte")
    print(data.inserted_id)
    print("obtengo el registro insertado")
    new_data = get_collection(account, entity_name).find_one({"_id": data.inserted_id})
    return new_data

# Retrieve a data with a matching ID
async def retrieve_data_id(account: Account, entity_name: str, id: str) -> dict:
    data = get_collection(account, entity_name).find_one({"_id": ObjectId(id)})
    if data:
        return data

# Update a data with a matching ID
async def update_data(account: Account, entity_name: str, id: str, newData: dict):
    # Return false if an empty request body is sent.
    # print(newData)
    if len(newData) < 1:
        return False
    data = get_collection(account, entity_name).find_one({"_id": ObjectId(id)})
    if data:
        updated_data = get_collection(account, entity_name).update_one(
            {"_id": ObjectId(id)}, {"$set": newData}
        )
        if updated_data:
            return True
        return False

# Delete a data from the database
async def delete_data(account: Account, entity_name: str, id: str):
    data = get_collection(account, entity_name).find_one({"_id": ObjectId(id)})
    if data:
        get_collection(account, entity_name).delete_one({"_id": ObjectId(id)})
        return True
