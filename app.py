import os
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------- LOAD DATA ----------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "worldfix_data.csv")

    df = pd.read_csv(csv_path)

    # clean data
    df = df.fillna("")

    print("CSV loaded successfully")

except Exception as e:
    print("CSV ERROR:", e)
    df = pd.DataFrame(columns=["Keywords", "Utterance", "Response"])


# ---------------- CHAT ROUTE ----------------
@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({"response": "Invalid request"}), 400

    user_text = data.get("message", "").lower().strip()
    username = data.get("username", "Guest")

    bot_reply = "I don't understand that yet. Try asking something else."

    # ---------------- SMART MATCHING ----------------
    for _, row in df.iterrows():

        keywords = str(row.get("Keywords", "")).lower().split(",")
        utterance = str(row.get("Utterance", "")).lower()
        response = str(row.get("Response", ""))

        # 1. Keyword matching
        keyword_match = any(word.strip() in user_text for word in keywords)

        # 2. Utterance full sentence matching
        utterance_match = utterance in user_text

        # if either matches → respond
        if keyword_match or utterance_match:
            bot_reply = response
            break

    return jsonify({
        "username": username,
        "response": bot_reply
    })


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)