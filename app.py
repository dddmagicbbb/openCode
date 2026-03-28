from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import json
from pathlib import Path

app = Flask(__name__)
TODO_FILE = Path("todos.json")

def load_todos():
    if TODO_FILE.exists():
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)

HTML = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: #1a1a2e; color: #eee; min-height: 100vh; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { text-align: center; margin-bottom: 30px; color: #00d9ff; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex: 1; padding: 12px; border: none; border-radius: 8px; 
                            background: #16213e; color: #fff; font-size: 16px; }
        input[type="text"]:focus { outline: 2px solid #00d9ff; }
        button { padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer;
                font-size: 14px; font-weight: bold; transition: 0.2s; }
        .btn-add { background: #00d9ff; color: #1a1a2e; }
        .btn-add:hover { background: #00b8d4; }
        .btn-del { background: #ff4757; color: #fff; padding: 6px 12px; font-size: 12px; }
        .btn-imp { background: #ffa502; color: #1a1a2e; padding: 6px 12px; font-size: 12px; }
        .todo-list { list-style: none; }
        .todo-item { display: flex; align-items: center; gap: 12px; padding: 16px; 
                    background: #16213e; border-radius: 12px; margin-bottom: 10px; }
        .todo-item.done { opacity: 0.5; }
        .todo-item.done .task { text-decoration: line-through; }
        .todo-item.important { border-left: 4px solid #ffa502; }
        .checkbox { width: 24px; height: 24px; cursor: pointer; accent-color: #00d9ff; }
        .task { flex: 1; font-size: 16px; }
        .important-mark { font-size: 20px; }
        .actions { display: flex; gap: 8px; }
        .empty { text-align: center; color: #666; padding: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>☀️ Todo App</h1>
        <form class="input-group" method="POST" action="/add">
            <input type="text" name="task" placeholder="할 일을 입력하세요..." required>
            <button type="submit" class="btn-add">추가</button>
        </form>
        <ul class="todo-list">
            {% if not todos %}
            <li class="empty">할 일이 없습니다.</li>
            {% endif %}
            {% for todo in todos %}
            <li class="todo-item {% if todo.done %}done{% endif %} {% if todo.important %}important{% endif %}">
                <a href="/toggle/{{ loop.index0 }}">
                    <input type="checkbox" class="checkbox" {% if todo.done %}checked{% endif %}>
                </a>
                <span class="task">{{ todo.task }}</span>
                <span class="important-mark">{% if todo.important %}☀️{% endif %}</span>
                <div class="actions">
                    <a href="/important/{{ loop.index0 }}"><button class="btn-imp">중요</button></a>
                    <a href="/delete/{{ loop.index0 }}"><button class="btn-del">삭제</button></a>
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''

@app.route("/")
def index():
    todos = load_todos()
    return render_template_string(HTML, todos=todos)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", "").strip()
    if task:
        todos = load_todos()
        todos.append({"task": task, "done": False, "important": False})
        save_todos(todos)
    return redirect(url_for("index"))

@app.route("/toggle/<int:index>")
def toggle(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
        save_todos(todos)
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return redirect(url_for("index"))

@app.route("/important/<int:index>")
def important(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["important"] = not todos[index]["important"]
        save_todos(todos)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
