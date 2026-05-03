from flask import Flask, render_template, request, redirect
import random
import sqlite3
import os
import uuid
import os

port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)

app = Flask(__name__)

os.makedirs("static/uploads", exist_ok=True)


def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT,
        text TEXT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_message(key, text, image):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO messages (key, text, image)
        VALUES (?, ?, ?)
    """, (key, text, image))

    conn.commit()
    conn.close()


def get_messages(key):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT text, image FROM messages WHERE key=?", (key,))
    data = c.fetchall()

    conn.close()
    return data


@app.route("/cindex")
def create_random_key():
    Random_key = "".join(str(random.randint(1, 9)) for _ in range(9))
    return render_template("cindex.html", Random_key=Random_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bindex")
def bindex():
    return render_template("bindex.html")


@app.route("/save", methods=["POST"])
def save():
    key = request.form["key"]   
    text = request.form["text"]
    file = request.files.get("image")

    image_path = None

    if file and file.filename != "":
        image_path = "static/uploads/" + str(uuid.uuid4()) + file.filename
        file.save(image_path)

    add_message(key, text, image_path)

    return f"Kaydedildi! Key: {key}"  

@app.route("/debug")
def debug():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM messages")
    data = c.fetchall()
    conn.close()
    return str(data)


@app.route("/endix")
def endix():
    return render_template("endix.html")

@app.route("/dindex")
def dindex():
    return render_template("dindex.html")

@app.route("/view", methods=["POST"])
def view():
    key = request.form["key"]

    data = get_messages(key)

    if not data:
        return render_template("dindex.html")

    return render_template("result.html", data=data)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
