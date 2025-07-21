from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("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")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    template = data.get("template", "")
    user_text = data.get("text", "")

    prompt = f"""
당신은 한국어 마케팅 문구 전문가입니다.
아래 내용을 광고 배너 문구로 다듬어 주세요. 반드시 한글로 작성하세요.

스타일 가이드: {template}
원본 문장: {user_text}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 마케팅 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        )

        generated_text = response.choices[0].message.content.strip()

        image_url = "https://via.placeholder.com/600x300.png?text=Banner+Preview"

        return jsonify({
            "text": generated_text,
            "image_url": image_url,
            "prompt": prompt
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
