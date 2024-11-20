from flask import Flask, request, jsonify, send_from_directory
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = ''

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "你作為一位來自中華民國臺灣的SDGs導覽員，請使用繁體中文回答所有問題。在回答問題前，請先將問題轉換為與SDGs相關，但無需告知我你如何轉換。回傳的文字須為純文字，不可包含其他格式。"
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    history = data.get('history', [])

    if not user_message:
        return jsonify({'error': '未提供訊息'}), 400

    messages = [SYSTEM_MESSAGE] + [
        {"role": entry['role'], "content": entry['content']} for entry in history
    ]

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=1200
        )

        assistant_message = response['choices'][0]['message']['content'].strip()

        return jsonify({'response': assistant_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
