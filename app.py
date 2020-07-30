from flask import Flask, redirect
from googleapiclient import discovery
from googleapiclient import discovery
from flask import render_template
from flask import request
import requests
import urllib.request
import re
from urllib.request import Request, urlopen
import time
from model import search_youtube
import model
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from flask_pymongo import PyMongo
from flask import session
import bcrypt
import json

# -- Initialization section --
app = Flask(__name__)
# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/aboutUs')
def aboutUs():
    return render_template("aboutUs.html")
@app.route('/upcycleSearch', methods=["GET", "POST"])
def upcycleSearch():
    return render_template("upcycleSearch.html")

@app.route('/upcycleResults', methods=["GET", "POST"])
def upcycleResults():

    if request.method == "POST":
        user_garment = request.form["garment"]
        user_brand = request.form["brand"]
        user_price = request.form["price"]
        if session["data"] != None and session["keys"] != None and session["garment"] == user_garment :
            search_results = session["data"]
            keys = session["keys"]
        else: 
            search_results = model.search_youtube(user_garment)
            session["data"] = search_results
            keys = list(search_results.keys())
            session["keys"] = keys
            session["garment"] = user_garment

        if session["scores"] != None and session["brand"] == user_brand:
            scores = session["scores"]
        else: 
            scores = model.parse_rating(user_brand)
            session["scores"] = scores
            session["brand"] = user_brand
        score = model.calculate_score(scores)
        return render_template('upcycleResults.html', score=score, scores=scores, keys=keys, search_results=search_results, user_garment=user_garment, user_brand=user_brand, user_price=user_price)
    else:
        return "Error. Nothing submitted. Please go back to the <a href='/upcycleSearch'>Upcycle Page</a>"

@app.route('/updateUserProgress', methods=["GET", "POST"])
def update_user_progress():
    username = session["username"]
    if request.method == "POST": 
        collection = mongo.db.users
        user = list(collection.find({"username":username}))
        user = user[0]
        new_env_score = user['env_score'] + int(request.form["env_score"])
        new_savings = user['savings'] + int(request.form["savings"])
        all_items = session["data"]
        fav_item_index = int(request.form["fav_item_index"])
        new_item = all_items[session["keys"][fav_item_index]]
        print(new_item)
        collection.update(
            {"username": username}, 
            {"$push": {"fav_items": new_item}}
        )
        collection.update({"username": username}, { "$set": {"savings": new_savings, "env_score": new_env_score}})
        env_score = user["env_score"]
        savings = user["savings"]
        fav_items = user["fav_items"]
        return render_template("userProfile.html", username = username,  env_score=env_score, savings=savings, fav_items=fav_items)    
    else: 
        return redirect("/")

app.secret_key = "k2u3gogsdboqasd34"
# name of database
app.config['MONGO_DBNAME'] = 'database'
# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:OmSyXfRK8jG98xVq@couture.zvxpp.mongodb.net/database?retryWrites=true&w=majority'
mongo = PyMongo(app)
@app.route("/loginsignup", methods=["GET", "POST"])
def loginsignup():
    if request.method == "GET":
        return render_template('login_signup.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        collection = mongo.db.users
        user = list(collection.find({"username":username}))
        if len(user) == 0:
            collection.insert_one({"username": username, "email":email, 
                                    "password": str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8'), 
                                    "savings":0, "env_score": 0, "fav_items":[]})
            session["username"] = username
            session["data"] = None
            session["scores"] = None
            session["keys"] = None
            dispText= "Welcome to the ctrl-alt-thread family, " + username + "!"
            return render_template("userProfile.html", dispText=dispText)
        elif bcrypt.hashpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')) == user[0]['password'].encode('utf-8'):
            session["username"] = username
            session["data"] = None
            session["scores"] = None
            session["keys"] = None
            user = user[0]
            env_score = user["env_score"]
            savings = user["savings"]
            fav_items = user["fav_items"]
            dispText= "Welcome back, " + username + "!"
            return render_template("userProfile.html", username = username, dispText=dispText,env_score=env_score, savings=savings, fav_items=fav_items )
        else:
          return "Error. Username and/or password is incorrect. <a href='/login_signup.html>login/signup</a> again"

@app.route("/logout", methods=["GET", "POST"])
def logout(): 
      session.clear()
      return render_template("index.html")

@app.route("/userProfile", methods=["GET", "POST"])
def userProfile():
    username = session["username"]
    collection = mongo.db.users
    user = list(collection.find({"username":username}))
    user = user[0]
    env_score = user["env_score"]
    savings = user["savings"]
    fav_items = user["fav_items"]
    return render_template("userProfile.html", username = username, env_score=env_score, savings=savings, fav_items=fav_items)