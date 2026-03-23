from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        text TEXT,
        completed INTEGER
    )""")

    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET"])
def home():
    if "user_id" in session:
        return render_template("index.html")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/todos", methods=["GET"])
def get_todos():
    user_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, text, completed FROM todos WHERE user_id=?", (user_id,))
    todos = c.fetchall()
    conn.close()

    return jsonify(todos)


@app.route("/add", methods=["POST"])
def add_todo():
    user_id = session.get("user_id")
    data = request.json

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO todos (user_id, text, completed) VALUES (?, ?, ?)",
              (user_id, data["text"], 0))
    conn.commit()
    conn.close()

    return "OK"


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_todo(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return "Deleted"


@app.route("/toggle/<int:id>", methods=["PUT"])
def toggle(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE todos SET completed = NOT completed WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return "Updated"


if __name__ == "__main__":
    app.run()