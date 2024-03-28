import asyncio
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import random
import json
from google.cloud import firestore
import re
import aiohttp

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_TOKEN)
db = firestore.Client()

async def post_to_slack_and_save_to_firestore(channel_id, user_id, user_name, ts, text, channel_name, triggered_words):
    try:
        # 채널 정보 가져오기
        channel_info = await client.conversations_info(channel=channel_id)
        channel_name = channel_info['channel']['name']
            
        # 랜덤 메시지 목록
        random_messages = [
            f"<@{user_id}>님, 이러시면 안돼요! :춘식눈물:\n님 호칭 사용을 실천해주세요 :루피하트:",
            "담당님 테스트중"
        ]
        
        # 랜덤 메시지 선택
        random_message = random.choice(random_messages)
        await client.chat_postMessage(
            channel=channel_id,
            text=random_message,
            thread_ts=ts  # 이 메시지를 스레드로 연결
        )

    except SlackApiError as e:
        print(f"Error posting message: {e}")

    # Firestore에 데이터 저장
    doc_ref = db.collection(u'slack_events').document()
    doc_ref.set({
        u'user_id': user_id,
        u'user_name': user_name,  # 사용자 이름 저장
        u'timestamp': ts,
        u'text': text,
        u'channel_id': channel_id,
        u'channel_name': channel_name,  # 채널 이름 저장
        u'triggered_words': triggered_words  # 트리거된 단어 저장
    })

@app.route('/slack/events', methods=['POST'])
async def slack_events():
    data = request.json
    trigger_words = ['선임님', '책임님', '팀장님', '담당님', '상무님', '전무님',
                    'CEO님', 'CTO님', '사장님', '사원님',
                    '위원님']
    trigger_words_pattern = '|'.join(trigger_words)

    if data['event']['type'] == 'message' and 'text' in data['event']:
        text = data['event']['text']
        channel_id = data['event']['channel']
        user_id = data['event']['user']
        ts = data['event']['ts']  # 메시지의 timestamp
        
        # 사용자 정보 가져오기
        user_info = await client.users_info(user=user_id)
        user_name = user_info['user']['real_name']
        
        if text in ['CA', 'ca', 'CA!', 'ca!']:
            try:
                await client.chat_postMessage(
                    channel=channel_id,
                    text="U+ CTO CA 여러분,\n오늘도 화이팅 하세요! :무너03:",
                )
            except SlackApiError as e:
                print(f"Error posting message: {e}")
        else:
            triggered_words = []
            for word in trigger_words:
                if word in text:
                    triggered_words.append(word)

            if triggered_words and not (user_name == "caca"): 
                await post_to_slack_and_save_to_firestore(channel_id, user_id, user_name, ts, text, '', triggered_words)

    return '', 200

if __name__ == '__main__':
    app.run()
