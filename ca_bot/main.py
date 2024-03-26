from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import random  # random 모듈 추가
import re

# 앞 패턴 정의
def extract_name(text):
    # 사용자 멘션(@)을 제거합니다. 이 경우, Slack의 멘션 형식을 고려해야 합니다.
    text = re.sub(r'<@\w+>', '', text)
    
    # 이름과 호칭을 추출하기 위한 정규 표현식을 수정합니다.
    pattern = re.compile(r'(\w+)(사원님|팀장님|책임님|담당님|상무님|전무님|CEO님|CTO님|사장님|위원님)(?!님들)')
    matches = pattern.findall(text)
    if matches:
        # 가장 첫 번째 매치에서 이름 부분만 추출합니다.
        return matches[0][0]
    else:
        # 매치가 없는 경우, None을 반환합니다.
        return None

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_TOKEN)

@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})

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
                response = client.chat_postMessage(
                    channel=channel_id,
                    text="U+ CTO CA 여러분,\n오늘도 화이팅 하세요! :무너03:",
                )
            except SlackApiError as e:
                print(f"Error posting message: {e}")
        elif any(word in text for word in trigger_words):
            # 랜덤 메시지 목록
            name = extract_name(text)
            random_messages = [
                f"<@{user_id}>님, 이러시면 안돼요! :춘식눈물:\n님 호칭 사용을 실천해주세요 :루피하트:",
                f"'{trigger_words}'은 없는 단어예요 :루피하트: 봄날같은 인사, ‘{name}님’과 함께 시작해보세요!"
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
