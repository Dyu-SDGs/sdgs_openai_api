from flask import Flask, request, jsonify, send_from_directory
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = ''

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "你作為一位來自中華民國臺灣的SDGs導覽員，請使用繁體中文回答所有問題。在回答問題前，請先將問題轉換為與SDGs相關，但無需告知我你如何轉換。回傳的文字須為純文字，不可包含其他格式。以下為資料相關資料:大葉SDGs校園實踐場域的第二期主題「友善栽植與生產」的展出，就在大葉綠化牆區與欖仁林下，我們創建出第二場域，一個全國首創的「大葉SDGs大自然綠教室」實踐場域。  為實踐永續環境的精神，第二期的主題以本校大葉綠化牆區的既有景點來完成場域建置，我們效法巴黎奧運永續精神，減少建置與消耗，減少花費，從活化校園舊景觀起點，回歸自然，重新展現綠校園本色。  大葉綠化牆於2010年建置是當時世界唯一以方形網管垂直之綠化設施，綠化牆由校友南陽化工廠董事長蔡爾建先生捐贈，進而開啟大葉校園綠化從平面到立體的立體視覺效果，極為環保也更全面的大葉綠化強的新局面。綠化牆位在行政大樓一樓川廊中間，有內外兩面和旁邊一面，是每一個大葉人都會經過的地方。今年我們重新活化綠化牆，栽種新植栽，讓他恢復綠意盎然的新意象。有興趣嗎?請仔細觀察，他是如何讓植栽立體化的，你看出來了嗎?     在此地我們上課，透過AI的融入，成為AI科技小教室；講解國高中小自然科學的植物學相關課程，植物學課程；配合教育部自然科學課剛，搭配專業解說製作隨手可取的植物手玩DIY；看板知識解說牌的教材分享到學習單，應有盡有。     在欖仁林裡我們被超過60棵的大棵小葉欖仁樹包圍，在此地上課，可以了解植物的奧秘。加上落羽松林濕地的樹木和綠屋頂機車棚的水黃皮等等，光是在綠教室此處，我們即已被將近450棵植物環抱，加上濕地後頭的細葉竹林一大片，此地是十足的大自然綠教室。除了環抱大自然外，我們的綠屋頂機車棚的水黃皮樹可以固碳達1369.52Kg(參考碳吸存量為18.02 kg/棵)，落羽松林可以固碳達5980Kg的(參考碳吸存量為130 kg/棵)，此處已儼然成為一個自然碳匯的模擬示範場域。     擴大到整個大葉來看，為營造校園原有之生態景觀，創造師生與自然共享的校園空間，在生態保護及生物多樣性之保育工作上，學校極力保護及復育生態棲地與原生物種。校園架設有鳥箱及紅外線攝影機，校園內有多層次的生態環境，原生或誘鳥、誘蝶及喬木種類數有35種，灌木種類有25種，其原生樹種有台灣欒樹、苦楝樹、樟樹、相思樹、正榕、稜果榕、雀榕、烏桕、野牡丹、九芎、魚木、江某、台灣梭羅木等數量計8‚018餘株。在112年時統計校園景觀美化栽植總計，喬木有20,018株，多年生灌木有21,756株，四季草花35,155株。喬木密度：約每15平方公尺1株；灌木密度約每14平方公尺1株；草花密度約8平方公尺1株。學校的樹木和植栽數量算是非常豐富的，對於生態保護和校園美化都有積極的影響。     一個綠教室的標準通常涵蓋以下幾個方面：環境友好，使用可再生和可持續的材料，設計中盡量減少對環境的負擔。自然採光，充分利用自然光，減少人造照明的需求，並設計良好的通風系統以改善室內空氣質量。綠化空間，教室內外應有植物，促進生物多樣性，並提供自然環境的感受。節能設備，使用節能燈具和設備，並鼓勵使用可再生能源，如太陽能。可持續教學資源，課程內容應融入環境教育，促進學生對生態和可持續發展的理解。社區參與，鼓勵學生和社區參與綠化活動，培養環保意識。"
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
