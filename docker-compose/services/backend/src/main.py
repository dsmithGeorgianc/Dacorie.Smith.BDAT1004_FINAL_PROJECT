import time
from datetime import datetime
from typing import Union

import motor
import uvicorn
from bson import ObjectId

from fastapi import FastAPI, HTTPException, Depends, Request


from src.stock_api.api_stock_caller import AsyncAPIMongoHelper
from src.database.quote_crud import QuotesCrud
from src.custom_setting.settings import Setting

from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

# Load settings when application starts
setting = Setting()
mongodb_url_str = setting.get_env('mongo_url')

motor = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url_str)



#. Build an API that serves data from the live cloud database1.

# Class should be able to use a URL to access the API and tes

# CORS configuration
origins = [
    "http://localhost:8080",
    "http://backend:8080"  # Assuming Vue.js is served on port 8080
    # Add any other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "Worldddddddd"}

@app.get("/store/pull_data_from_api")
async def snippets_search_by_text():
    try:
        helper = AsyncAPIMongoHelper()

        list_of_stocks = ['AI','AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

        for  stock in list_of_stocks :
            stock_symbol = stock  # Example stock symbol
            api_key = "9ec31ab87e3107ecf50cd316d110f93b"  # Your API key
            api_url = helper.build_api_url(stock_symbol, api_key)

            api_data = await helper.get_jsonparsed_data(api_url)

            await helper.store_data_in_mongo(api_data)

        return {"success_full": True}
    except Exception as e:

        print(f"An error occurred: {e}")
        # raise HTTPException(status_code=500, detail=f"An error occurred: {e}")+
        return {"success_full": False}


@app.get("/store/quotes/all")
async def snippets_all():
    try:
        helper = QuotesCrud(motor)
        data = await helper.get_all()

        return {"data": data}
    except Exception as e:

        print(f"An error occurred: {e}")
        # raise HTTPException(status_code=500, detail=f"An error occurred: {e}")+
        return {"success_full": False, 'data': e}


@app.get("/store/quotes/get_item_by_id/{id}")
async def snippets_all(object_id: str):
    try:
        helper = QuotesCrud(motor)
        object_id = ObjectId(object_id)

        snippets = await helper.find('_id',object_id)

        return {"data": snippets}
    except Exception as e:

        print(f"An error occurred: {e}")
        # raise HTTPException(status_code=500, detail=f"An error occurred: {e}")+
        return {"success_full": False,'data':e}

@app.get("/store/quotes/get_item_by_symbol/{symbol}")
async def snippets_all_id(symbol: str):
    try:
        helper = QuotesCrud(motor)


        snippets = await helper.find('symbol',symbol)

        return {"data": snippets}
    except Exception as e:

        print(f"An error occurred: {e}")
        # raise HTTPException(status_code=500, detail=f"An error occurred: {e}")+
        return {"success_full": False,'data':e}

## Get a range of items3.
@app.get("/search_by_date_range/")
async def search_by_date_range(start_date: str, end_date: str):
    try:
        helper = QuotesCrud(motor)

        start_timestamp = int(time.mktime(datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
        end_timestamp = int(time.mktime(datetime.strptime(end_date, "%Y-%m-%d").timetuple()))

        query = {"timestamp": {"$gte": start_timestamp, "$lte": end_timestamp}}

        snippets = await helper._get_documents(query=query)

        return {"data": snippets}
    except Exception as e:

        print(f"An error occurred: {e}")
        # raise HTTPException(status_code=500, detail=f"An error occurred: {e}")+
        return {"success_full": False, 'data': e}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
