from flask import Flask, request, jsonify, send_from_directory
import openai, os
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API')

with open('system_message.txt', 'r', encoding='utf-8') as file:
    system_message_content = file.read()

SYSTEM_MESSAGE = {
    "role": "system",
    "content": system_message_content
}

user_histories = {}

def clean_old_histories():
    """刪除超過一小時未活動的用戶歷史紀錄"""
    now = datetime.now()
    to_delete = [
        ip for ip, data in user_histories.items()
        if now - data['last_active'] > timedelta(hours=1)
    ]
    for ip in to_delete:
        del user_histories[ip]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': '未提供訊息'}), 400

    user_ip = request.remote_addr

    clean_old_histories()

    if user_ip not in user_histories:
        user_histories[user_ip] = {
            'history': [],
            'last_active': datetime.now()
        }

    user_histories[user_ip]['last_active'] = datetime.now()
    history = user_histories[user_ip]['history']

    messages = [SYSTEM_MESSAGE] + [
        {"role": entry['role'], "content": entry['content']} for entry in history
    ]
    messages.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=1200
        )

        assistant_message = response['choices'][0]['message']['content'].strip()
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": assistant_message})

        return jsonify({'response': assistant_message.replace("\n", "")})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
