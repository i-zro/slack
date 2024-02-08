from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_TOKEN)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    trigger_words = ['선임', '책임', '팀장', '담당', '상무', '전무']

    # 메시지 이벤트 처리
    if data['event']['type'] == 'message' and 'text' in data['event']:
        text = data['event']['text']
        channel_id = data['event']['channel']
        user_id = data['event']['user']
        ts = data['event']['ts']  # 메시지의 timestamp

        if text == 'CA' or text == 'ca':
            try:
                response = client.chat_postMessage(
                    channel=channel_id,
                    text="유플러스 CA, 오늘도 좋은 하루 되세요!",
                    thread_ts=ts  # 이 메시지를 스레드로 연결
                )
            except SlackApiError as e:
                print(f"Error posting message: {e}")
        elif any(word in text for word in trigger_words):
            try:
                response = client.chat_postMessage(
                    channel=channel_id,
                    text=f"<@{user_id}>님, 이러시면 안돼요! :춘식눈물: 님 호칭 사용을 실천해주세요 :루피하트:",  # 멘트
                )
            except SlackApiError as e:
                print(f"Error posting message: {e}")

    return '', 200

if __name__ == '__main__':
    app.run()
