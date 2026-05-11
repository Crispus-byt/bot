import os
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "worldfix_data.csv")
    df = pd.read_csv(csv_path)
    print("CSV loaded successfully")
except Exception as e:
    print("CSV ERROR:", e)
    df = pd.DataFrame(columns=["Keywords", "Response"])


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if not data:
        return jsonify({"response": "Invalid request"}), 400

    user_text = data.get("message", "").lower()
    username = data.get("username", "Guest")

    bot_reply = "I don't understand that yet. Try asking something else."

    for _, row in df.iterrows():
        keywords = str(row['Keywords']).split(',')

        for word in keywords:
            if word.strip().lower() in user_text:
                bot_reply = row['Response']
                break

        if bot_reply != "I don't understand that yet. Try asking something else.":
            break

    return jsonify({
        "username": username,
        "response": bot_reply
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)