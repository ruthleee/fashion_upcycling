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
from model import search_youtube, login_signup
import model
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
        search_results = model.search_youtube(user_garment)
        return render_template('upcycleResults.html', user_garment=user_garment, user_brand=user_brand, user_price=user_price)
    else:
        return "Error. Nothing submitted. Please go back to the <a href='/upcycleSearch'>Upcycle Page</a>"




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
        email = request.form["email"]
        dispText = login_signup(username, password)
        if dispText=="Error":
            return "Error. Username and/or password is incorrect. <a href='/login_signup.html>login/signup</a> again"
        else:
            return render_template("userProfile.html", dispText=dispText)
        