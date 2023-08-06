import requests
import urllib3
from PIL import Image
import os
import time
import datetime
import random
import hashlib
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("config.json") as f:
    config = json.load(f)

cookie = str(config.get("cookie"))
image = str(config.get("image"))
upload_num = int(config.get("upload_num"))

def log(text):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}")

def get_token(session):
    response = session.get("https://www.roblox.com/build/upload", verify=False)
    try:
        start_index = response.text.find("__RequestVerificationToken")
        if start_index != -1:
            start_value = response.text.find('value="', start_index) + len('value="')
            end_value = response.text.find('"', start_value)
            veri = response.text[start_value:end_value]
        else:
            raise ValueError("Token not found")
    except Exception as e:
        print("Error fetching verification token:", e)
        return None
    return veri

def upload_decal(cookie, location, name, session):
    token = get_token(session)
    if not token:
        return
    files = {"file": (f"final/{name}.png", open(location, "rb"), "image/png")}
    data = {"__RequestVerificationToken": token, "assetTypeId": "13", "isOggUploadEnabled": "True", "isTgaUploadEnabled": "True", "onVerificationPage": "False", "captchaEnabled": "True", "name": name, "description":"emppu"}
    try:
        response = session.post("https://www.roblox.com/build/upload?assetTypeId=13&nl=true", files=files, data=data)
        response.raise_for_status()
        log(f"Uploaded `{name}` successfully")
    except requests.exceptions.RequestException as e:
        log(f"Error sending the request")

with open("words.txt", "r") as file:
    word_list = file.read().splitlines()

with open("useragents.txt", "r") as file:
    useragents = file.read().splitlines()

for root, dirs, files in os.walk("final"):
    for file in files:
        os.remove(os.path.join(root, file))

def hash_file(filename):
   h = hashlib.sha1()
   with open(filename, "rb") as file:
       for chunk in iter(lambda: file.read(1024), b""): h.update(chunk)
   return h.hexdigest()

with requests.Session() as session:
    session.cookies.update({".ROBLOSECURITY": cookie})
    for i in range (upload_num):
        randomnum = random.randrange(0, 1000000)
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
            time.sleep(5)
