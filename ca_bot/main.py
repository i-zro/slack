import re
from flask import Flask, request, jsonify, make_response
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import random

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_TOKEN)

def get_user_name_from_mention(text):
    mentions = re.findall(r'<@(\w+)>', text)
    names = []
    for user_id in mentions:
        try:
            response = client.users_info(user=user_id)
            if response["ok"]:
                names.append(response["user"]["real_name"])
        except SlackApiError as e:
            print(f"Slack API 에러: {e}")
    return names

def extract_name(text):
    # 멘션된 사용자 이름이 있는 경우, 그 이름을 반환.
    names_from_mention = get_user_name_from_mention(text)
    if names_from_mention:
        return names_from_mention[0]

    # 멘션된 사용자 이름이 없는 경우, 원래 로직을 따름.
    text_without_mention = re.sub(r'<@\w+>', '', text)
    pattern = re.compile(r'([가-힣A-Za-z]+)\s*(사원님|팀장님|책임님|담당님|상무님|전무님|CEO님|CTO님|사장님|위원님)(?!\s*님들)')
    matches = pattern.findall(text_without_mention)
    for match in matches:
        # '님들'이 포함되지 않은 호칭으로 끝나는 이름 추출
        return match[0]
    return None

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    trigger_words = ['선임님', '책임님', '팀장님', '담당님', '상무님', '전무님', 'CEO님', 'CTO님', '사장님', '사원님', '위원님']

    if data['event']['type'] == 'message' and 'text' in data['event']:
        text = data['event']['text']
        channel_id = data['event']['channel']
        user_id = data['event']['user']
        ts = data['event']['ts']

        trigger_word_found = any(word in text for word in trigger_words)
        triggered_word = [word for word in trigger_words if word in text]

        if trigger_word_found:
            custom_message = f"<@{user_id}>님, :춘식눈물:\n {triggered_word[0]}보다는 님 호칭 사용이 어떨까요?" if triggered_word else None
            
            random_messages = [
                f"<@{user_id}>님, 이러시면 안돼요! :춘식눈물:\n님 호칭 사용을 실천해주세요 :루피하트:",
            ]

            # 사용자의 메시지 내용에 기반한 맞춤 메시지가 있다면 random_messages 리스트에 추가
            if custom_message:
                random_messages.append(custom_message)

            # 랜덤 메시지 중 하나 선택하여 발송
            random_message = random.choice(random_messages)
            client.chat_postMessage(channel=channel_id, text=random_message, thread_ts=ts)

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
