from flask import Flask, request, jsonify, make_response  # make_response 추가
import json  # json 모듈 추가
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import random
import re  # re 모듈 추가

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_TOKEN)

def extract_name(text):
    text = re.sub(r'<@\w+>', '', text)
    pattern = re.compile(r'(\w+)\s*(사원님|팀장님|책임님|담당님|상무님|전무님|CEO님|CTO님|사장님|위원님)(?!님들)')
    matches = pattern.findall(text)
    if matches:
        return matches[0][0]
    else:
        return None

@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return jsonify(challenge=slack_event["challenge"])
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    trigger_words = ['선임님', '책임님', '팀장님', '담당님', '상무님', '전무님', 'CEO님', 'CTO님', '사장님', '사원님', '위원님']

    if data['event']['type'] == 'message' and 'text' in data['event']:
        text = data['event']['text']
        channel_id = data['event']['channel']
        user_id = data['event']['user']
        ts = data['event']['ts']

        name = extract_name(text)  # 이름 추출
        if name:  # 이름이 추출된 경우만 처리
            trigger_word_found = [word for word in trigger_words if word in text]
            if trigger_word_found:
                # 실제 트리거된 단어를 사용하여 메시지 생성
                random_messages = [
                    f"<@{user_id}>님, 이러시면 안돼요! :춘식눈물:\n님 호칭 사용을 실천해주세요 :루피하트:",
                    f"봄날같은 인사, ‘{name}님’과 함께 시작해보세요!"
                ]
                random_message = random.choice(random_messages)
                try:
                    response = client.chat_postMessage(
                        channel=channel_id,
                        text=random_message,
                        thread_ts=ts
                    )
                except SlackApiError as e:
                    print(f"Error posting message: {e}")

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
