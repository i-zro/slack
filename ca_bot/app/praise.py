from app import app, client, db
from flask import request, jsonify
import datetime

def save_praise(user_id, praised_user, reason):
    # Firestore에 칭찬 정보 저장
    doc_ref = db.collection(u'praises').document()
    doc_ref.set({
        u'user_id': user_id,
        u'praised_user': praised_user,
        u'reason': reason,
        u'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/slack/great', methods=['POST'])
def slack_great():
    # 요청에서 데이터 추출
    user_id = request.form.get('user_id')
    text = request.form.get('text').strip().split(' ', 1)
    
    if len(text) < 2:
        return jsonify({
            "response_type": "ephemeral",
            "text": "사용법: /칭찬해요 @유저명 칭찬사유"
        })

    praised_user, reason = text
    save_praise(user_id, praised_user, reason)
    
    return jsonify({
        "response_type": "in_channel",  # 응답이 채널에 표시되도록 설정
        "text": f"{praised_user}님이 칭찬 받았습니다! 🎉\n사유: {reason}"
    })
