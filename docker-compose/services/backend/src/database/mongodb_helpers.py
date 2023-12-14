import asyncio
import json
import motor.motor_asyncio
import pymongo
import pprint

from bson import json_util
from pymongo import cursor

from src.custom_setting.settings import Setting


class MongodbHelper:
    client = motor.motor_asyncio.AsyncIOMotorClient()
    database = ''
    collection = ''

    def __init__(self, client_url: str, database_name: str, collection_str: str, motor_client):
        # self.client = pymongo.MongoClient(client_url)
        # self.client = motor.motor_asyncio.AsyncIOMotorClient(client_url, uuidRepresentation="standard")
        # self.client = motor_client

        setting = Setting()
        mongodb_url_str = setting.get_env('mongo_url')
        self.client = motor.motor_asyncio.AsyncIOMotorClient(client_url, uuidRepresentation="standard")

        self.database = self.client[database_name]
        self.collection = self.database[collection_str]

    def check_if_database_exist(self, database: str):
        dblist = self.client.list
        if database in dblist:
            return True
        else:
            return False

    def check_if_collection_exist(self, collection: str):
        collist = self.database.list_collection_names()
        if collection in collist:
            return True
        else:
            return False

    '''
     # check to see if a value already exist in the mongodb by comparing the values by hashing them then compare the
      hashingthem
    '''

    async def check_if_document_exist_by_hash(self, collection_to_compare):

        collection_to_compare_hash = hash(json.dumps(collection_to_compare, default=json_util.default))

        for item in list(await self.all()):
            item.pop('_id')

            market_hash = hash(json.dumps(item, default=json_util.default))
            # print(market_hash)

            if market_hash == collection_to_compare_hash:
                # print("Found")
                return True
        return False

    async def check_if_document_exist_by_hash_pop_date(self, collection_to_compare):

        collection_to_compare_hash = hash(json.dumps(collection_to_compare, default=json_util.default))

        for item in list(await self.all()):
            item.pop('_id')
            item.pop('date_created')
            market_hash = hash(json.dumps(item, default=json_util.default))
            # print(market_hash)

            if market_hash == collection_to_compare_hash:
                # print("Found")
                return True
        return False

    async def insert_collection(self, item):
        self.collection.insert_one(item)

    async def insert_multiple_collection(self, collection):
        self.collection.insert_many(collection)

    async def sort(self, query, limit):
        cursor = self.collection.find({}, {"_id": 0}).sort(query).limit(limit)
        result = []
        for document in await cursor.to_list(length=None):
            result.append(document)
        return result

    async def count_documents(self, query):
        return self.collection.count_documents(query)

    async def find_sort(self, query, args, sort):
        cursor = self.collection.find(query, args).sort(sort)
        result = []
        for document in await cursor.to_list(length=None):
            result.append(document)
        return result

    async def find(self, query, args):
        cursor = self.collection.find(query, args)
        result = []
        for document in await cursor.to_list(length=None):
            result.append(document)
        return result

    async def all(self):
        cursor = self.collection.find()
        result = []
        for document in await cursor.to_list(length=None):
            result.append(document)
        return result

    async def distinct(self, key):
        cursor = self.collection.distinct(key)
        result = []
        for document in await cursor.to_list():
            result.append(document)
        return result

    async def distinct_with_key(self, key):
        cursor = self.collection.distinct(key)
        result = []
        for document in await cursor.to_list():
            result.append(document)
        return result

    def create_index(self, index):
        return self.collection.create_index(index)

    def drop_index(self, index):
        return self.collection.drop_index(index)

#
# setting = Setting()
# mongodb_url_str = setting.get_env('mongo_url')
# database_name_str = "canada_dividend"
# client = motor.motor_asyncio.AsyncIOMotorClient()
# #
# mongodb = MongodbHelper(client_url=mongodb_url_str, database_name=database_name_str,
#                         collection_str="stocks", motor_client=client)
# #
# # print(mongodb.find({}, {}))
# # mresult = mongodb.all()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(mongodb.all())
