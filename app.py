from flask import Flask, render_template, request, redirect
import sqlite3
import logging

# ---------------- Logging Setup ----------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

def get_db():
    return sqlite3.connect("todo.db")

# ---------------- Home Route ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        task = request.form["task"]
        cur.execute("INSERT INTO todo (task) VALUES (?)", (task,))
        conn.commit()
        logging.info(f"Task added: {task}")

    cur.execute("SELECT * FROM todo")
    tasks = cur.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

# ---------------- Mark Complete ----------------
@app.route("/complete/<int:id>")
def complete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE todo SET status='Completed' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    logging.info(f"Task completed: ID {id}")
    return redirect("/")

# ---------------- Delete Task ----------------
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todo WHERE id=?", (id,))
    conn.commit()
    conn.close()

    logging.warning(f"Task deleted: ID {id}")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
