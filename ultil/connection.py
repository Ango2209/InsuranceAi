import pymongo
##mongodb
mongo_url="mongodb+srv://Anhngo2208:Anhngole.123@cluster0.onhfeyv.mongodb.net/sentiment?retryWrites=true&w=majority"

def init_connection():
    return pymongo.MongoClient(mongo_url)