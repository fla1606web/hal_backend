import datetime
import jwt
import pytz
from server.models.login import Login
from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

client = MongoClient(config("mongo.host"))
database = client[config("mongo.database")]

user_collection = database.get_collection("users")
 
secret = "fEEFF!-gas$3fsd**1212$4dEE"
tz = pytz.timezone("America/Lima")

async def exits_user(login: Login):
        print(login)
        user = user_collection.find_one({"user": login.username, "password": login.password})
        return user

def generate_token(id_account: str, id_user: str, is_administrator: bool, login: Login):
        payload = {
            'iat': datetime.datetime.now(tz=tz),
            'exp': datetime.datetime.now(tz=tz) + datetime.timedelta(minutes=30),
            'username': login.username,
            'password': login.password,
            'id_user': id_user,
            'id_account': id_account,
            'is_administrator': str(is_administrator)
        }
        return jwt.encode(payload, secret, algorithm="HS256")
    

def verify_token(headers):
        if 'authorization' in headers.keys():
            authorization = headers['authorization']
            encoded_token = authorization.split(" ")[1]
            print(encoded_token)
            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, secret, algorithms=["HS256"])
                    
                    return True
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError, jwt.DecodeError):
                    return False

        return False

 
def renew_token(token: str):
        # The token is empty
        if (len(token) > 0):
            # Decode token and verify that it is expired
            try:
                payload_previous = jwt.decode(token, secret, algorithms=["HS256"])
                # returns the same token
                return token
            except (jwt.ExpiredSignatureError):
                # The token has expired. Renew the token                
                payload_previous = jwt.decode(token, options={"verify_signature": False})
                payload = {
                    'iat': datetime.datetime.now(tz=tz),
                    'exp': datetime.datetime.now(tz=tz) + datetime.timedelta(minutes=30),
                    'username': payload_previous['username'],
                    'password': payload_previous['password'],
                    'id_user': payload_previous['id_user'],
                    'id_account': payload_previous['id_account'],
                    'is_administrator': payload_previous['is_administrator']
                }
                return jwt.encode(payload, secret, algorithm="HS256")            
            except (jwt.InvalidSignatureError, jwt.DecodeError):
                # The token is invalid
                return ""
        
        return token
