import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load your chatbot dataset
df = pd.read_csv('worldfix_data.csv')


@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({"response": "Invalid request"}), 400

    user_text = data.get("message", "").lower()
    username = data.get("username", "Guest")

    # ---- BOT LOGIC ----
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


# IMPORTANT FOR RENDER
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)