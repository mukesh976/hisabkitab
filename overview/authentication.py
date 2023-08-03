from rest_framework import authentication
from rest_framework import exceptions
from pymongo import MongoClient
from bson.objectid import ObjectId

class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
            
        try:
            token = authorization_header.split(' ')[1]
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
            
        client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/<dbname>")
        db = client.<dbname>
        user_collection = db['user']
        user = user_collection.find_one({'_id': ObjectId(payload['user_id'])})
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
            
        return (user, token)
