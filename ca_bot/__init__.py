from flask import Flask
from slack_sdk import WebClient
import os
from google.cloud import firestore

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_TOKEN)
db = firestore.Client()
