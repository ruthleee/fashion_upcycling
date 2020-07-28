# ---- YOUR APP STARTS HERE ----
# -- Import section --
# AIzaSyCSsfexfhI7I3r-MXUuSmD3_0oVRNLjs1s
from flask import Flask
from googleapiclient import discovery
from googleapiclient import discovery
from flask import render_template
from flask import request
import requests
import urllib.request
import re
from urllib.request import Request, urlopen
import time
from model import youtube_search
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from flask_pymongo import PyMongo
from flask import session
import bcrypt




# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/upcycleSearch', methods=["GET", "POST"])
def upcycleSearch():
    
    return render_template("upcycleSearch.html")
@app.route('/upcycleResults', methods=["GET", "POST"])
def upcycleResults():
    if request.method == "POST":
        user_garment = request.form["garment"]
        user_brand = request.form["brand"]
        user_price = request.form["price"]
        return render_template('upcycleResults.html', user_garment=user_garment, user_brand=user_brand, user_price=user_price)
    else:
        return "Error. Nothing submitted. Please go back to the <a href='/upcycleSearch'>Upcycle Page</a>"
@app.route('/parsehub')
def parsehub():
    params = {
        "api_key": "tAgMZD_gGfMN",
        "format": "json",
        "project_token": "tTunoV0JjdT4",
        "start_url": "https://directory.goodonyou.eco/brand/the-r-collective",
        "send_email": "1"
    }
    r = requests.post("https://www.parsehub.com/api/v2/projects/tTunoV0JjdT4/run", data=params)
    run_token = r.json()["run_token"]
    p = requests.get('https://www.parsehub.com/api/v2/runs/' + run_token, params=params)
    for i in range(10): 
        time.sleep(1)
        p = requests.get('https://www.parsehub.com/api/v2/runs/' + run_token, params=params)
        if p.json()["data_ready"] == 1: 
            break
    
    print(p.text)
    final_data = requests.get("https://www.parsehub.com/api/v2/projects/tTunoV0JjdT4/last_ready_run/data", params=params)
    print(final_data.text)
    return("hellour")

@app.route('/parse_url')
def parse_url(): 
    url = 'https://www2.hm.com/en_us/productpage.0876657002.html'
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = Request(url=url, headers=headers) 
    html = urlopen(req).read() 
    soup = BeautifulSoup(html, 'lxml')
    type(soup)
    title = soup.title
    print(title)
    head_elem = soup.find('h1')
    print(head_elem.text)
    def contains_price(s3):
     return ("$" in s3)
    print(soup.find_all(string=contains_price))
    return ("hello")
    # print(soup.find_all('html'))
    # text = soup.get_text()
    # print(text.strip('\n'))
    # prices = soup.find_all('span')
    # print(prices)
    # Print out the text
    # text = soup.get_text()
    # print(soup.text)
@app.route("/parse_rating")
def parse_rating():
    params = {
        "api_key": "tAgMZD_gGfMN",
        "format": "json",
        "project_token": "tTunoV0JjdT4",
        "start_url": "https://directory.goodonyou.eco/brand/the-r-collective",
        "send_email": "1"
    }
    r = requests.post("https://www.parsehub.com/api/v2/projects/tTunoV0JjdT4/run", data=params)
    run_token = r.json()["run_token"]
    p = requests.get('https://www.parsehub.com/api/v2/runs/' + run_token, params=params)
    for i in range(10): 
        time.sleep(1)
        p = requests.get('https://www.parsehub.com/api/v2/runs/' + run_token, params=params)
        if p.json()["data_ready"] == 1: 
            break
    
    print(p.text)
    final_data = requests.get("https://www.parsehub.com/api/v2/projects/tTunoV0JjdT4/last_ready_run/data", params=params)
    print(final_data.text)
    return("hellour")
<<<<<<< HEAD
=======

app.secret_key = "k2u3gogsdboqasd34"
# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:OmSyXfRK8jG98xVq@couture.zvxpp.mongodb.net/database?retryWrites=true&w=majority'

mongo = PyMongo(app)
@app.route("/loginsignup", methods=["GET", "POST"])
def loginsignup():
    session.clear()
    if request.method == "GET":
        return render_template('login_signup.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        collection = mongo.db.users
        user = list(collection.find({"username":username}))
        if len(user) == 0:
            collection.insert_one({"username": username, "password": str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8')})
            session["username"] = username
            return("Welcome as a new user")
        elif bcrypt.hashpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')) == user[0]['password'].encode('utf-8'):
            session["username"] = username
            return"Welcome back! Go to <a href='/index'>home</a>."
        else:
            return "Error"
>>>>>>> 2fccbe802d52bfc4958e0accfb6ab6be01743bea

app.secret_key = "k2u3gogsdboqasd34"
# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:OmSyXfRK8jG98xVq@couture.zvxpp.mongodb.net/database?retryWrites=true&w=majority'

mongo = PyMongo(app)
@app.route("/loginsignup", methods=["GET", "POST"])
def loginsignup():
    session.clear()
    if request.method == "GET":
        return render_template('login_signup.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        collection = mongo.db.users
        user = list(collection.find({"username":username}))
        if len(user) == 0:
            collection.insert_one({"username": username, "password": str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8')})
            session["username"] = username
            return("Welcome as a new user")
        elif bcrypt.hashpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')) == user[0]['password'].encode('utf-8'):
            session["username"] = username
            return"Welcome back! Go to <a href='/index'>home</a>."
        else:
            return "Error"