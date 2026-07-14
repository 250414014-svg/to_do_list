from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==================================================
# STRUKTUR DATA
# ==================================================

# SD1 : Daftar tugas
# Menyimpan seluruh task yang dibuat user
tasks = []

# SD2 : STACK UNDO
# Menyimpan riwayat aksi terakhir
# Prinsip LIFO (Last In First Out)
undo_stack = []

# SD3 : STACK REDO
# Menyimpan aksi yang sudah di-Undo
# agar bisa dikembalikan lagi
redo_stack = []


# ==================================================
# HALAMAN UTAMA
# ==================================================

@app.route("/")
def index():
    return render_template("index.html")


# ==================================================
# MENAMPILKAN SEMUA TASK
# ==================================================

@app.route("/tasks")
def get_tasks():
    return jsonify(tasks)


# ==================================================
# TAMBAH TASK
# ==================================================

@app.route("/add", methods=["POST"])
def add_task():

    data = request.json

    task = {
        "text": data["text"],
        "done": False
    }

    # Menambahkan task ke daftar
    tasks.append(task)

    # Simpan aksi ke Undo Stack
    undo_stack.append({
        "action": "add",
        "task": task
    })

    # Kosongkan Redo Stack
    redo_stack.clear()

    return jsonify({
        "success": True
    })


# ==================================================
# EDIT TASK
# ==================================================

@app.route("/edit/<int:index>", methods=["POST"])
def edit_task(index):

    if 0 <= index < len(tasks):

        data = request.json

        old_text = tasks[index]["text"]

        # Mengubah isi task
        tasks[index]["text"] = data["text"]

        # Simpan ke Undo Stack
        undo_stack.append({
            "action": "edit",
            "index": index,
            "old_text": old_text,
            "new_text": data["text"]
        })

        redo_stack.clear()

    return jsonify({
        "success": True
    })


# ==================================================
# HAPUS TASK
# ==================================================

@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_task(index):

    if 0 <= index < len(tasks):

        # Menghapus task
        removed = tasks.pop(index)

        # Simpan data ke Undo Stack
        undo_stack.append({
            "action": "delete",
            "task": removed,
            "index": index
        })

        redo_stack.clear()

    return jsonify({
        "success": True
    })


# ==================================================
# TANDAI SELESAI / BELUM SELESAI
# ==================================================

@app.route("/toggle/<int:index>", methods=["POST"])
def toggle_task(index):

    if 0 <= index < len(tasks):

        old_status = tasks[index]["done"]

        # Mengubah status task
        tasks[index]["done"] = not old_status

        # Simpan ke Undo Stack
        undo_stack.append({
            "action": "toggle",
            "index": index,
            "old_status": old_status
        })

        redo_stack.clear()

    return jsonify({
        "success": True
    })


# ==================================================
# UNDO
# ==================================================

@app.route("/undo", methods=["POST"])
def undo():

    # Jika stack kosong
    if not undo_stack:
        return jsonify({
            "success": False
        })

    # Mengambil aksi terakhir
    # dari Undo Stack (LIFO)
    action = undo_stack.pop()

    # ==========================
    # Undo Tambah Task
    # ==========================
    if action["action"] == "add":

        if tasks:
            tasks.pop()

    # ==========================
    # Undo Hapus Task
    # ==========================
    elif action["action"] == "delete":

        tasks.insert(
            action["index"],
            action["task"]
        )

    # ==========================
    # Undo Status Task
    # ==========================
    elif action["action"] == "toggle":

        idx = action["index"]

        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = action["old_status"]

    # ==========================
    # Undo Edit Task
    # ==========================
    elif action["action"] == "edit":

        idx = action["index"]

        if 0 <= idx < len(tasks):
            tasks[idx]["text"] = action["old_text"]

    # Simpan ke Redo Stack
    redo_stack.append(action)

    return jsonify({
        "success": True
    })


# ==================================================
# REDO
# ==================================================

@app.route("/redo", methods=["POST"])
def redo():

    # Jika stack kosong
    if not redo_stack:
        return jsonify({
            "success": False
        })

    # Mengambil aksi terakhir
    # dari Redo Stack (LIFO)
    action = redo_stack.pop()

    # ==========================
    # Redo Tambah Task
    # ==========================
    if action["action"] == "add":

        tasks.append(
            action["task"]
        )

    # ==========================
    # Redo Hapus Task
    # ==========================
    elif action["action"] == "delete":

        idx = action["index"]

        if 0 <= idx < len(tasks):
            tasks.pop(idx)

    # ==========================
    # Redo Toggle Status
    # ==========================
    elif action["action"] == "toggle":

        idx = action["index"]

        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = not action["old_status"]

    # ==========================
    # Redo Edit Task
    # ==========================
    elif action["action"] == "edit":

        idx = action["index"]

        if 0 <= idx < len(tasks):
            tasks[idx]["text"] = action["new_text"]

    # Simpan kembali ke Undo Stack
    undo_stack.append(action)

    return jsonify({
        "success": True
    })


# ==================================================
# FILTER TASK
# ==================================================

@app.route("/filter/<status>")
def filter_task(status):

    if status == "done":

        result = [
            task for task in tasks
            if task["done"]
        ]

    elif status == "undone":

        result = [
            task for task in tasks
            if not task["done"]
        ]

    else:

        result = tasks

    return jsonify(result)


# ==================================================
# MENJALANKAN FLASK
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)