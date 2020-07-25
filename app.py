# ---- YOUR APP STARTS HERE ----
# -- Import section --
# AIzaSyCSsfexfhI7I3r-MXUuSmD3_0oVRNLjs1s
from flask import Flask
# from flask import render_template
# from flask import request
from googleapiclient import discovery
# from flask import render_template
# from flask import request
from googleapiclient import discovery

from flask import render_template
from flask import request
import requests
import urllib.request
import re
from urllib.request import Request, urlopen




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
@app.route('/parsehub')
def parsehub():
    params = {
        "api_key": "tAgMZD_gGfMN",
        "format": "json",
        "project_token": "tTunoV0JjdT4",
        "start_url": "https://directory.goodonyou.eco/brand/reformation",
        "send_email": "1"

    }
    r = requests.post("https://www.parsehub.com/api/v2/projects/tTunoV0JjdT4/run", data=params)
    print(r.json["run_token"])
    # p = requests.get('https://www.parsehub.com/api/v2/projects/tTunoV0JjdT4/last_ready_run/data', params=params)
    # print(p.text)
    return("hello)")
@app.route('/webS')
def webS():
    req = Request('http://pythonprogramming.net/parse-website-using-regular-expressions-urllib/', headers={'User-Agent': 'Mozilla/5.0'})
    respData = urlopen(req).read()
    # url = 'https://directory.goodonyou.eco/brand/white-house-black-market'

    # req = urllib.request.Request(url)
    # resp = urllib.request.urlopen(req)
    # respData = resp.read()
    rated = re.findall(r'<p>(.*?)</p>',str(respData))
    # <span class="StyledText-sc-1sadyjn-0 bBUTWf">Rated: Not Good Enough</span>
    print(rated)
    # for eachR in rated:
    #     print(eachR)
    return("hellur")



