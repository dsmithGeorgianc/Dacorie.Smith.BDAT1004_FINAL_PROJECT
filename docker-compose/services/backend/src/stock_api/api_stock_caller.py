import json
import aiohttp
import motor
from motor.motor_asyncio import AsyncIOMotorClient

from src.custom_setting.settings import Setting
from src.database.mongodb_helpers import MongodbHelper


class AsyncAPIMongoHelper:
    async def get_jsonparsed_data(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                return json.loads(data)

    async def store_data_in_mongo(self, data):

        setting = Setting()
        mongodb_url_str = setting.get_env('mongo_url')
        database_name_str = "canada_dividend"
        client = motor.motor_asyncio.AsyncIOMotorClient()
        #
        mongodb = MongodbHelper(client_url=mongodb_url_str, database_name=database_name_str,
                                collection_str="stocks", motor_client=client)
        #

        await mongodb.insert_multiple_collection(data)
        return data

    def build_api_url(self,stock_symbol, api_key):
        base_url = "https://financialmodelingprep.com/api/v3/quote/"
        return f"{base_url}{stock_symbol}?apikey={api_key}"



#
# # Usage example
# import asyncio
#
# async def main():
#
#     helper = AsyncAPIMongoHelper()
#
#     stock_symbol = "AAPL"  # Example stock symbol
#     api_key = "9ec31ab87e3107ecf50cd316d110f93b"  # Your API key
#     api_url = helper.build_api_url(stock_symbol, api_key)
#
#     api_data = await helper.get_jsonparsed_data(api_url)
#     await helper.store_data_in_mongo(api_data)
#     print(api_data)
#
#
# asyncio.run(main())
# #
#
# url = ("https://financialmodelingprep.com/api/v3/quote/AAPL?apikey=9ec31ab87e3107ecf50cd316d110f93b")
# # Usage example
# #api_url = "https://financialmodelingprep.com/api/v3/search?query=AA&apikey=your_api_key"
# mongo_uri = "your_mongo_uri"
# db_name = "your_db_name"
# collection_name = "your_collection_name"
#
# helper = APIMongoHelper(mongo_uri, db_name, collection_name)
# api_data = helper.get_jsonparsed_data(url)
# print(api_data)
# #helper.store_data_in_mongo(api_data)