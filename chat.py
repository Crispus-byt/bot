import pandas as pd
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Load your CSV once (IMPORTANT: not inside route)
df = pd.read_csv('worldfix_data.csv')


@app.route('/chat', methods=['POST'])
def chat():

    user_text = request.form['message'].lower()

    # Optional: get username safely
    username = request.form.get('username', 'Guest')

    # Connect DB (only if you really need it)
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

    # If user not found
    if not user:
        return jsonify({"response": "User not found. Please sign up first."})

    # ---- BOT LOGIC ----
    found_answer = False
    bot_reply = "I don't understand that yet. Try asking about posting or payments."

    for index, row in df.iterrows():

        keywords_list = str(row['Keywords']).split(',')

        for word in keywords_list:
            clean_word = word.strip().lower()

            if clean_word in user_text:
                bot_reply = row['Response']
                found_answer = True
                break

        if found_answer:
            break

    return jsonify({
        "username": username,
        "response": bot_reply
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)