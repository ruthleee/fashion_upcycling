from googleapiclient import discovery
from urllib.request import Request, urlopen
import time
import requests
import urllib.request
import re
from flask import Flask
from flask_pymongo import PyMongo
from flask import session
import json
import bcrypt
app = Flask(__name__)
api_key="AIzaSyBS_-xa-p0IOcqqvv_sIkwBSZgYN4y2qhU"
#cntrl alt thread api_key = "AIzaSyDai2vPdaNi_bG3ej-2YVt1dDky5IEOrk8" out of quota: 10:14 AM PST, Julyy 29th
#old: fashion api_key = "AIzaSyCSsfexfhI7I3r-MXUuSmD3_0oVRNLjs1s"
youtube = discovery.build('youtube', 'v3', developerKey=api_key)
def search_youtube(item_name, num_queries=5):
    # api_key = "AIzaSyDai2vPdaNi_bG3ej-2YVt1dDky5IEOrk8"
    # #old: fashion api_key = "AIzaSyCSsfexfhI7I3r-MXUuSmD3_0oVRNLjs1s"
    # youtube = discovery.build('youtube', 'v3', developerKey=api_key)
    queries = [" DIY", "  Thrift Flip", " Upcycle Tutorial"]
    #num_results = 0 
    search_results = {}
    for query in queries: 
        search_by = item_name + query
        request = youtube.search().list(q=search_by, part='snippet', type='video', maxResults=num_queries, pageToken=None)
        result = request.execute() 
        #num_results += result['pageInfo.totalResults']
        items = result['items']
        for each_item in items: 
            search_results[each_item["snippet"]["title"]] = {"video_url": "https://www.youtube.com/watch?v=" + each_item["id"]["videoId"], 
                                                            "description": each_item["snippet"]["description"], 
                                                            "thumbnail_url": each_item["snippet"]["thumbnails"]["high"]["url"],
                                                            "title": each_item["snippet"]["title"] }
        if len(search_results) > 0 and query =="  Thrift Flip": 
            print("didn't make third query")
            break
    # print(type(search_results))
    if len(search_results) == 0: 
        return "No upcycling tutorials were found for '" +  item_name + ".' Please try searching with a different item name."
    else: 
        return search_results
def parse_rating(item_brand):
    formatted = item_brand.lower().replace("&", "and")
    brand_to_parse = formatted.split() 
    url_brand_key = brand_to_parse[0]
    if len(brand_to_parse) > 1: 
        for i in range(1,  len(brand_to_parse)):
            url_brand_key += "-" + brand_to_parse[i]
    params = {
        "api_key": "tAgMZD_gGfMN",
        "format": "json",
        "project_token": "tTunoV0JjdT4",
        "start_url": "https://directory.goodonyou.eco/brand/" + url_brand_key,
        "send_email": "0"
    }
    r = requests.post("https://www.parsehub.com/api/v2/projects/tTunoV0JjdT4/run", data=params)
    run_token = r.json()["run_token"]
    p = requests.get('https://www.parsehub.com/api/v2/runs/' + run_token, params=params)
    for i in range(10): 
        time.sleep(1)
        p = requests.get('https://www.parsehub.com/api/v2/runs/' + run_token, params=params)
        if p.json()["data_ready"] == 1: 
            break
    final_data = requests.get("https://www.parsehub.com/api/v2/projects/tTunoV0JjdT4/last_ready_run/data", params=params)
    ratings = final_data.json()
    scores = {}
    scores = {"planet": [int(ratings["planetRate"][0]), ratings["exp_planetRate"]],
              "people": [int(ratings["peopleRate"][0]), ratings["exp_peopleRate"]],
              "animal": [int(ratings["animalRate"][0]), ratings["exp_animalRate"]]}
    # print(scores)
    return scores
app.config['MONGO_DBNAME'] = 'database'
# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:OmSyXfRK8jG98xVq@couture.zvxpp.mongodb.net/database?retryWrites=true&w=majority'
mongo = PyMongo(app)
def login_signup(username, password, email):
        collection = mongo.db.users
        user = list(collection.find({"username":username}))
        if len(user) == 0:
            collection.insert_one({"username": username, "email":email, "password": str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8'), "savings":0, "env_score": 0})
            session["username"] = username
            return("Welcome as a new user, " + "user")
        elif bcrypt.hashpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')) == user[0]['password'].encode('utf-8'):
            session["username"] = username
            # foo = 12
            # collection.update({"username": "user5"},{ "$set": {"savings": foo,  "env_score": 5}})
            return"Welcome back, " + username + "!"
        else:
            return "Error"
def calculate_score(scores):
    print(scores['planet'][0])
    print(scores["animal"][0])
    print(scores["people"][0])
    numerator = scores["planet"][0] + scores["people"][0] + scores["animal"][0]
    return int((float(numerator)/15.0)*100.0)