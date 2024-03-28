from app import app, client, db
from flask import request, jsonify
import datetime

def save_praise(user_id, user_name, praised_user, reason):
    # Firestore에 칭찬 정보 저장
    doc_ref = db.collection(u'praises').document()
    doc_ref.set({
        u'user_id': user_id,
        u'user_name': user_name,
        u'praised_user': praised_user,
        u'reason': reason,
        u'timestamp': datetime.datetime.utcnow().isoformat()
    })

@app.route('/slack/great', methods=['POST'])
def slack_great():
    # 요청에서 데이터 추출
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')  # Assuming you can get the username from the request
    text = request.form.get('text').strip().split(' ', 1)
    
    if len(text) < 2:
        return jsonify({
            "response_type": "ephemeral",
            "text": "사용법: /칭찬해요 @유저명 칭찬사유"
        })

    praised_user, reason = text
    save_praise(user_id, user_name, praised_user, reason)
    
    # Send initial ephemeral response to the user who invoked the command
    response = {
        "response_type": "ephemeral",
        "text": f"{praised_user}님이 칭찬 받았습니다! 🎉\n사유: {reason}"
    }
    client.chat_postMessage(channel=request.form['channel_id'], **response)

    # Send follow-up in-channel response visible to everyone in the channel
    response["response_type"] = "in_channel"
    client.chat_postMessage(channel=request.form['channel_id'], **response)

    return '', 200
