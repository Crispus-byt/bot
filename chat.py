import pandas as pd
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

df = pd.read_csv('worldfix_data.csv')


@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({"response": "Invalid request"}), 400

    user_text = data.get("message", "").lower()
    username = data.get("username", "Guest")

    # ---- DATABASE SAFE CONNECTION ----
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='znest'
        )

        cursor = connection.cursor()
        cursor.execute(
            "SELECT username FROM users WHERE username=%s",
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            return jsonify({"response": "User not found. Please sign up first."})

    except Exception as e:
        return jsonify({"response": "Database error"}), 500

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)