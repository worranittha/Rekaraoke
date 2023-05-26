# https://dev.to/daltonic/how-to-build-a-predictive-machine-learning-site-with-react-and-python-part-two-api-development-11d2
# import library
import uvicorn                                  # use to create a server (communicat with API and HTTP request and response)
from pydantic import BaseModel                  # use to identify API request parameters (ensure right data types)
from fastapi import FastAPI                     # use to define routes and funcitons (define response for a request)
from fastapi.middleware.cors import CORSMiddleware   # use to define the resoure domains from API
from models import *
import requests

# initialize fastAPI
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# define model input types
class InputData(BaseModel):
    text: str

# set up home route
@app.get("/")
def read_root():
    return {"data": "Welcome to re-karaoke online"}

# set up initial model route
@app.get("/initial/")
def init():
    init_model()
    return 'Already initial'

# set up prediction route
@app.post("/prediction/")
async def get_predict(data: InputData):
    # model
    sample = data.text
    result = predict(sample)
    # print('result:', result)

    # genius api
    client_access_token = "oOMj3H44xLpw7_tsy-EH15SKhn0i8_9_H25jGHHrcUYbe3_fAfwjK2eyIWfF2b6i"
    genius_search_url = f"http://api.genius.com/search?q={result}&access_token={client_access_token}"
    response = requests.get(genius_search_url)
    json_data = response.json()
    try:
        song_name = json_data['response']['hits'][0]['result']['full_title']
    except:
        song_name = 'Cannot find this song!'
    print('song name:', song_name)

    return {"data": {'prediction': song_name, 'interpretation': 'Get your answer!'}}

# config server host and port
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
