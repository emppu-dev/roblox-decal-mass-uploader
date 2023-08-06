import os
import time
import datetime

packages = ["requests","urllib3","pillow"]

def log(text):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}")

for package in packages:
    try:
        __import__(package)
        log(f"`{package}` is already installed")
    except ImportError:
        log(f"Installing `{package}`")
        os.system(f"pip install {package}")
