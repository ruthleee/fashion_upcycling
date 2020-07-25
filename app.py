# ---- YOUR APP STARTS HERE ----
# -- Import section --
# AIzaSyCSsfexfhI7I3r-MXUuSmD3_0oVRNLjs1s
from flask import Flask

# from flask import render_template
# from flask import request
from googleapiclient import discovery

from flask import render_template
from flask import request



# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/upcycleSearch')
def upcycleSearch():
    return render_template("upcycleSearch.html")
app.route('/youtube')
def youtube():

    api_key = "AIzaSyC6rqXcj4ZRxEBW_t-mPzr_3G4ei25HtO8"
    youtube = discovery.build('youtube', 'v3', developerKey=api_key)
    # req = youtube.search().list(q='machine learning tutorial', part='snippet', type='video', maxResults=50, pageToken=None)
    # res = req.execute()
    MAX_COUNT = 10
    nextPageToken =  None
    #items[query number]['id']['videoId']
    #items[query number]['snippet']['title]
    #items[query number]['snippet']['description']
    #items[query number]['snippet']['description']['thumbnails']['high']['url'] (['width'], ['height'])

    search_by = 'DIY crop hoodie'
    for i in range(1):
        req = youtube.search().list(q=search_by, part='snippet', type='video', maxResults=MAX_COUNT, pageToken=nextPageToken)
        res = req.execute()
        nextPageToken = res['nextPageToken']
        items = res['items']
        if res['nextPageToken'] == None:
            break; # exit from the loop
        # print(items[0])
        # print(items[0]['id']['videoId'])
        # print(items[0]['snippet']['title'])
        # print(items[0]['snippet']['description'])
        # print(items[0]['snippet']['thumbnails']['high']['url'])

        for each_item in items:
            #store in DB or file or print the same.
            # print (each_item['id']['videoId'])
            print(each_item['id']['videoId'])
            print(each_item['snippet']['title'])
            print(each_item['snippet']['description'])
            print(each_item['snippet']['thumbnails']['high']['url'])
    return "hello world"



