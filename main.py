import requests
from PIL import Image
import os
import time
import datetime
import random
import hashlib
import json

with open("config.json") as f:
    config = json.load(f)

cookie = str(config.get("cookie"))
image = str(config.get("image"))
upload_num = int(config.get("upload_num"))

def log(text):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}")

def welcome(session):
    if not os.path.exists(image):
        log("No image found")
        quit()
    try:
        bot = session.get('https://www.roblox.com/mobileapi/userinfo').json()["UserName"]
        log(f"Welcome `{bot}`")
    except:
        log("Invalid cookie")
        quit()

def get_token(session):
    response = session.post('https://friends.roblox.com/v1/users/1/request-friendship')
    if 'x-csrf-token' in response.headers:
        return response.headers['x-csrf-token']
    else:
        log('x-csrf-token not found')

def upload_decal(cookie, location, name, session):
    try:
        headers = {"Requester": "Client","X-CSRF-TOKEN": get_token(session)}
        response = session.post(f"https://data.roblox.com/data/upload/json?assetTypeId=13&name={name}&description=emppu", data=open(location, 'rb'), headers=headers)
        response.raise_for_status()
        log(f"Uploaded `{name}` successfully")
    except requests.exceptions.RequestException as e:
        if response.status_code == 429:
            log(f"Ratelimited, waiting 60 seconds")
            time.sleep(60)
        log(f"Error sending the request")

with open("words.txt", "r") as file:
    word_list = file.read().splitlines()

with open("useragents.txt", "r") as file:
    useragents = file.read().splitlines()

for root, dirs, files in os.walk("final"):
    for file in files:
        os.remove(os.path.join(root, file))

def hash_file(filename):
   h = hashlib.sha256()
   with open(filename, "rb") as file:
       for chunk in iter(lambda: file.read(1024), b""):
           h.update(chunk)
   return h.hexdigest()

with requests.Session() as session:
    session.cookies.update({".ROBLOSECURITY": cookie})
    welcome(session)
    for i in range (upload_num):
        randomnum = random.randrange(0, 99999999999999)
        img = Image.open(image)
        img2 = img.resize((420+i,420+i), Image.LANCZOS)
        img2.save(f"final/{randomnum}.png")
        time.sleep(0.15)
        message = hash_file(f"final/{randomnum}.png")
        log(f"{message} - {randomnum}.png")
    for root, dirs, files in os.walk("final"):
        for file in files:
            useragent = random.choice(useragents)
            session.headers.update({"User-Agent": useragent})
            name = random.choice(word_list)
            upload_decal(cookie, os.path.join("final", file), name, session)
            time.sleep(1.5)
