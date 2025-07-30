from flask import Flask, request, jsonify
import base64
import pandas as pd
from io import BytesIO
import openai

app = Flask(__name__)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/reviewinvestasi", methods=["POST"])
def review():
    data = request.get_json()
    file_b64 = data.get("file_content_base64")

    file_bytes = base64.b64decode(file_b64)
    df = pd.read_excel(BytesIO(file_bytes), sheet_name="Keekonomian")

    irr = df.iloc[0]["IRR Project"]
    npv = df.iloc[0]["NPV"]

    prompt = f"Tinjau proyek investasi berikut:\nIRR: {irr}%\nNPV: {npv}\nApakah proyek ini layak? Berikan ringkasan."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content
    return jsonify({"review_result": result})
