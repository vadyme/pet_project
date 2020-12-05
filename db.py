from flask_pymongo import pymongo

CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.llv79.mongodb.net/<db_name>?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('<db_name>')
fixtures_db_collection = pymongo.collection.Collection(db, '<collection_name>')