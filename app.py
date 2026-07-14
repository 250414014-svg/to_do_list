from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

tasks = []
undo_stack = []
redo_stack = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks")
def get_tasks():
    return jsonify(tasks)

@app.route("/add", methods=["POST"])
def add_task():

    data = request.json

    task = {
        "text": data["text"],
        "done": False
    }

    tasks.append(task)

    undo_stack.append({
        "action": "add",
        "task": task
    })

    redo_stack.clear()

    return jsonify({"success": True})

@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_task(index):

    if 0 <= index < len(tasks):

        removed = tasks.pop(index)

        undo_stack.append({
            "action": "delete",
            "task": removed,
            "index": index
        })

        redo_stack.clear()

    return jsonify({"success": True})

@app.route("/toggle/<int:index>", methods=["POST"])
def toggle_task(index):

    tasks[index]["done"] = not tasks[index]["done"]

    return jsonify({"success": True})

@app.route("/undo", methods=["POST"])
def undo():

    if not undo_stack:
        return jsonify({"success": False})

    action = undo_stack.pop()

    if action["action"] == "add":
        tasks.pop()

    elif action["action"] == "delete":
        tasks.insert(action["index"], action["task"])

    redo_stack.append(action)
~~
    return jsonify({"success": True})

@app.route("/redo", methods=["POST"])
def redo():

    if not redo_stack:
        return jsonify({"success": False})

    action = redo_stack.pop()

    if action["action"] == "add":
        tasks.append(action["task"])

    elif action["action"] == "delete":

        if action["index"] < len(tasks):
            tasks.pop(action["index"])

    undo_stack.append(action)

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)