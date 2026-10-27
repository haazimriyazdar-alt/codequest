import sqlite3
from flask import Flask, render_template_string, request

app = Flask(__name__)
DB = "codequest.db"

QUESTIONS = [
    {"q": "What does print(2 + 3) show?", "options": ["5", "23", "Error"], "answer": "5"},
    {"q": "Which one is a Python list?", "options": ["[1, 2, 3]", "(1, 2, 3)", "{1, 2, 3}"], "answer": "[1, 2, 3]"},
    {"q": "Which keyword starts a loop over items?", "options": ["for", "loop", "repeat"], "answer": "for"},
    {"q": "What does len('hello') return?", "options": ["5", "4", "6"], "answer": "5"},
    {"q": "Which symbol starts a comment?", "options": ["#", "//", "--"], "answer": "#"},
]

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CodeQuest</title>
<style>
  body { font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 20px; }
  .wrap { max-width: 700px; margin: auto; }
  h1 { color: #38bdf8; margin-bottom: 0; }
  .sub { color: #94a3b8; margin-top: 4px; }
  .card { background: #1e293b; border-radius: 12px; padding: 20px; margin: 18px 0; }
  .score { background: #16a34a; color: white; border-radius: 12px; padding: 16px; font-size: 20px; text-align: center; }
  input[type=text] { padding: 10px; border-radius: 8px; border: none; width: 100%; box-sizing: border-box; }
  label { display: block; padding: 8px 10px; margin: 4px 0; background: #334155; border-radius: 8px; cursor: pointer; }
  label:hover { background: #475569; }
  button { background: #38bdf8; color: #0f172a; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; }
  button:hover { background: #7dd3fc; }
  ol { padding-left: 24px; }
  li { padding: 6px 0; }
</style>
</head>
<body>
<div class="wrap">
  <h1>CodeQuest</h1>
  <p class="sub">Test your Python skills and climb the leaderboard!</p>

  {% if score is not none %}
    <div class="score">Well done {{ name }}! Your score: {{ score }} / {{ questions|length }}</div>
  {% endif %}

  <form method="post">
    <div class="card">
      <b>Your name</b><br><br>
      <input type="text" name="name" maxlength="30" placeholder="Enter your name" required>
    </div>
    {% for q in questions %}
      {% set qi = loop.index0 %}
      <div class="card">
        <b>{{ loop.index }}. {{ q.q }}</b><br><br>
        {% for opt in q.options %}
          <label><input type="radio" name="q{{ qi }}" value="{{ opt }}"> {{ opt }}</label>
        {% endfor %}
      </div>
    {% endfor %}
    <button type="submit">Submit answers</button>
  </form>

  <div class="card">
    <h2>Leaderboard</h2>
    <ol>
      {% for row in board %}
        <li>{{ row[0] }} - {{ row[1] }}</li>
      {% else %}
        <li>No scores yet. Be the first!</li>
      {% endfor %}
    </ol>
  </div>
</div>
</body>
</html>
"""

def get_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER)")
    return conn

@app.route("/", methods=["GET", "POST"])
def home():
    score = None
    name = ""
    conn = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()[:30] or "Anonymous"
        score = 0
        for i, q in enumerate(QUESTIONS):
            if request.form.get(f"q{i}") == q["answer"]:
                score += 1
        conn.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        conn.commit()
    board = conn.execute("SELECT name, score FROM scores ORDER BY score DESC, id ASC LIMIT 10").fetchall()
    conn.close()
    return render_template_string(PAGE, questions=QUESTIONS, score=score, name=name, board=board)

if __name__ == "__main__":
    app.run(debug=True)