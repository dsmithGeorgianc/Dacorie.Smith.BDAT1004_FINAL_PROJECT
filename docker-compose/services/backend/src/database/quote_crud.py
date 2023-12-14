import asyncio
from datetime import datetime, timedelta, date

import motor.motor_asyncio

from src.helpers.date_helper.date_heplers import DateHelpers
from src.custom_setting.settings import Setting
from src.database.mongodb_helpers import MongodbHelper

import redis
import json

import logging

from src.helpers.redis_helper.redis_helper import RedisHelper

logger = logging.getLogger(__name__)


class QuotesCrud:
    setting = Setting()
    mongodb_url_str = setting.get_env('mongo_url')
    database_name_str = "canada_dividend"
    mongodb = ''


    def __init__(self, motor_client):
        self.mongodb = MongodbHelper(client_url=self.mongodb_url_str, database_name=self.database_name_str,
                                     collection_str="stocks", motor_client=motor_client)

    async def _get_documents(self, query={}, projection={"_id": 0}, sort=("date_created", -1)):
        try:
            cursor = self.mongodb.collection.find(query, projection).sort(*sort)
            documents = await cursor.to_list(length=None)
            return documents
        except Exception as e:
            logger.error(f"An error occurred while getting documents: {e}")
            raise e

    async def get_all(self) -> list:
        # snippets = self.r.get("snippets")
        return await self._get_documents()


    async def get_categories(self) -> list:
        categories = await self.mongodb.collection.distinct("categories")
        return categories

    async def find(self, attribute, data):
        documents = await self._get_documents({attribute: {'$eq': data}})
        return documents

    async def insert(self, question, model_ai_name, description, categories, tags, answer):
        try:
            if await self.find(attribute="question", data=question) == 0:
                item = {
                    "question": question,
                    "is_public": True,
                    "description": description,
                    "model_ai_name": model_ai_name,
                    "tags": tags,
                    "categories": categories,
                    "favorites": 0,
                    "createdOn": datetime.now(DateHelpers.get_jamaica_timezone()),
                    "answer": answer
                }
                self.mongodb.insert_collection(item)
                return True
            return False
        except Exception as e:
            logger.error(f"An error occurred while inserting document: {e}")
            raise e

    async def search(self, query):
        # results = await self._get_documents({"$text": {"$search": query}})
        # return list(results)

        # Attempt to fetch from Redis
        redis_helper = RedisHelper()
        snippets = redis_helper.get_from_cache(query)  # Get data from cache

        if snippets:
            print(query)
            return json.loads(snippets)
        else:
            print("Cache miss")
            # Fetch data from DB (or another source)
            snippets = await self._get_documents({"$text": {"$search": query}})
            transforms_arr = []

            for snippet in snippets:
                # Format the datetime object to a desired string format
                formatted_str = snippet['createdOn'].strftime("%A, %B %d, %Y %I:%M:%S %p")

                transforms_arr.append({
                    "is_public": snippet['is_public'],
                    "description": snippet['description'],
                    "model_ai_name": snippet['model_ai_name'],
                    "tags": snippet['tags'],
                    "categories": snippet['categories'],
                    "favorites": snippet['favorites'],
                    "answer": snippet['answer'],
                    "question": snippet['question'],
                    "imageUrl": snippet['categories'],
                    "dateTime": formatted_str
                })

            # Cache the result in Redis for 1 hour (3600 seconds)
            # self.r.setex("snippets", 360, json.dumps(transforms_arr))
            redis_helper.set_to_cache(query, json.dumps(transforms_arr), 3600)
            return snippets

            # return await self._get_documents()

    async def create_text_indexes(self):
        try:
            # Create text indexes for the desired fields
            await self.mongodb.collection.create_index([
                ("question", "text"),
                ("description", "text"),
                ("tags", "text"),
                ("categories", "text"),
                ("answer", "text")
            ])
            print("Text indexes created successfully.")
        except Exception as e:
            logger.error(f"An error occurred while creating text indexes: {e}")
            raise e



# text = OpenaiRandomTweet()
# fact=text.send_tweet()



# setting = Setting()
# mongodb_url_str = setting.get_env('mongo_url')
# client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url_str)
# crud = QuotesCrud(client)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(crud.insert(fact,"topic","Topic"))













