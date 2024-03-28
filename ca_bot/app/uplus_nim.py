from app import app, client, db
from flask import request, jsonify
import threading
import random
import datetime
import re

now = datetime.datetime.now()

def process_event(data):
    # 트리거 단어 목록
    trigger_words = ['선임님', '책임님', '팀장님', '담당님', '상무님', '전무님',
                    'CEO님', 'CTO님', '사장님', '사원님', '위원님']
    
    text = data['event']['text']
    # '님들'로 끝나는 모든 단어 제거
    text_without_nimdeul = re.sub(r'\b\w+님들\b', '', text)
    channel_id = data['event']['channel']
    user_id = data['event']['user']
    ts = data['event']['ts']

    # 사용자 정보 가져오기
    user_info = client.users_info(user=user_id)
    user_name = user_info['user']['real_name']
    
    if text in ['CA', 'ca', 'CA!', 'ca!']:
        try:
            response = client.chat_postMessage(
                channel=channel_id,
                text="U+ CTO CA 여러분,\n오늘도 화이팅 하세요! :무너03:",
            )
        except SlackApiError as e:
            print(f"Error posting message: {e}")
    else:
        triggered_words = [word for word in trigger_words if word in text_without_nimdeul]
    
        if triggered_words and not (user_name == "caca"):
            channel_info = client.conversations_info(channel=channel_id)
            channel_name = channel_info['channel']['name']
            triggered_words_s = ', '.join(triggered_words)

            random_messages = [
                f"<@{user_id}>님, 이러시면 안돼요! :춘식눈물:\n님 호칭 사용을 실천해주세요 :루피하트:",
                f"{triggered_words_s}보다는 님이라고 부를 때, 수평적/창의적 의견 공유에 한걸음 가까워져요! :kirby_dance-9961:",
                f"님은 갔지마는 나는 님을 보내지 아니하였습니다. :루피눈물2: (님좀 써주십쇼 :기도:)",
                f"자꾸 이렇게 님 호칭 사용에 비 협조적 이시라면... 내년 CA 의장은 바로 <@{user_id}>님!:point_right: 바로 당신! :firecracker: \n(24/3/29 부로 차곡차곡 기록중입니다)"
            ]
            random_message = random.choice(random_messages)
            try:
                response = client.chat_postMessage(
                    channel=channel_id,
                    text=random_message,
                    thread_ts=ts
                )
                # Firestore에 저장
                doc_ref = db.collection(u'slack_events').document()
                now_kst = datetime.now(pytz.timezone('Asia/Seoul'))
                doc_ref.set({
                    u'user_id': user_id,
                    u'user_name': user_name,
                    u'timestamp_kst': now_kst.isoformat(),
                    u'text': text,
                    u'channel_id': channel_id,
                    u'channel_name': channel_name,
                    u'triggered_words': triggered_words
                })
            except SlackApiError as e:
                print(f"Error posting message: {e}")

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    threading.Thread(target=process_event, args=(data,)).start()
    return jsonify({'status': 'ok'}), 200
