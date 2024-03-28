from google.cloud import secretmanager
from google.oauth2.service_account import Credentials
import gspread
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import random
import json

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_TOKEN)

def get_secret(secret_name):
    """Google Cloud Secret Manager에서 Secret 값을 조회합니다."""
    client = secretmanager.SecretManagerServiceClient()
    project_id = "main-nucleus-413512"  # 여기에 실제 Google Cloud 프로젝트 ID를 입력하세요.
    name = f"projects/627744097884/secrets/GOOGLE_APPLICATION_CREDENTIALS_JSON/latest"
    response = client.access_secret_version(request={"name": name})
    secret_string = response.payload.data.decode("UTF-8")
    return secret_string

def initialize_gspread():
    """Secret Manager에서 조회한 서비스 계정 키를 사용하여 gspread 클라이언트를 초기화합니다."""
    secret_name = "GOOGLE_APPLICATION_CREDENTIALS_JSON"
    service_account_info = get_secret(secret_name)
    credentials_dict = json.loads(service_account_info)
    credentials = Credentials.from_service_account_info(credentials_dict)
    gc = gspread.authorize(credentials)
    return gc

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    trigger_words = ['선임님', '책임님', '팀장님', '담당님', '상무님', '전무님',
                    'CEO님', 'CTO님', '사장님', '사원님',
                    '위원님']

    if data['event']['type'] == 'message' and 'text' in data['event']:
        text = data['event']['text']
        channel_id = data['event']['channel']
        user_id = data['event']['user']
        ts = data['event']['ts']  # 메시지의 timestamp

        if text in ['CA', 'ca', 'CA!', 'ca!']:
            try:
                gc = initialize_gspread()
                response = client.chat_postMessage(
                    channel=channel_id,
                    text="U+ CTO CA 여러분,\n오늘도 화이팅 하세요! :무너03:",
                )
            except SlackApiError as e:
                print(f"Error posting message: {e}")
        elif any(word in text for word in trigger_words):
            # 랜덤 메시지 목록
            random_messages = [
                f"<@{user_id}>님, 이러시면 안돼요! :춘식눈물:\n님 호칭 사용을 실천해주세요 :루피하트:"
            ]
            try:
                # 랜덤 메시지 선택
                random_message = random.choice(random_messages)
                response = client.chat_postMessage(
                    channel=channel_id,
                    text=random_message,
                    thread_ts=ts  # 이 메시지를 스레드로 연결
                )
            except SlackApiError as e:
                print(f"Error posting message: {e}")

    return '', 200

if __name__ == '__main__':
    app.run()
