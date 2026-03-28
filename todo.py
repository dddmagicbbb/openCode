import pick
import json
from pathlib import Path

TODO_FILE = Path.home() / ".todo.json"

def load_todos():
    if TODO_FILE.exists():
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def format_todo(item, index):
    status = "✓" if item["done"] else "○"
    important = "☀️ " if item.get("important", False) else ""
    done_text = "[완료]" if item["done"] else ""
    return f"{index+1}. [{status}] {important}{item['task']} {done_text}"

def main():
    while True:
        todos = load_todos()
        
        if not todos:
            options = ["할 일 추가", "종료"]
            option, index = pick.pick(options, title="Todo App", indicator=">")
            
            if index == 0:
                task = input("\n할 일 입력: ").strip()
                if task:
                    todos.append({"task": task, "done": False, "important": False})
                    save_todos(todos)
            else:
                break
        else:
            options = [format_todo(t, i) for i, t in enumerate(todos)]
            options.append("+ 할 일 추가")
            
            selected, index = pick.pick(options, title="Todo App (v:완료 d:삭제 i:중요)", indicator=">", multiselect=False)
            
            if selected == "+ 할 일 추가":
                task = input("\n할 일 입력: ").strip()
                if task:
                    todos.append({"task": task, "done": False, "important": False})
                    save_todos(todos)
            else:
                action = input(f"\n작업 (v:완료 d:삭제 i:중요): ").strip().lower()
                
                if action == "v":
                    todos[index]["done"] = not todos[index]["done"]
                    save_todos(todos)
                elif action == "d":
                    todos.pop(index)
                    save_todos(todos)
                elif action == "i":
                    todos[index]["important"] = not todos[index]["important"]
                    save_todos(todos)

if __name__ == "__main__":
    main()
