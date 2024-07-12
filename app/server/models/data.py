import json
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

def ResponseModel(data, message):
    json_object = parse_json(data) 

    return {
        "data": json_object,
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
