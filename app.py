from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/notes", methods=["GET"])
def get_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = [{"id": row[0], "content": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(notes)


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json
    content = data.get("content")

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes(content) VALUES(?)", (content,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note saved!"})


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"message": "Note not found."}), 404

    return jsonify({"message": "Note deleted!"})


if __name__ == "__main__":
    app.run(debug=True)
