// ── Animasi debu ───────────────────────────────────────────
const dustEl = document.getElementById('dust');
for (let i = 0; i < 18; i++) {
    const s = document.createElement('span');
    const size = Math.random() * 4 + 2;
    s.style.cssText = `
        width:${size}px; height:${size}px;
        left:${Math.random()*100}%;
        animation-duration:${8+Math.random()*14}s;
        animation-delay:${Math.random()*12}s;
    `;
    dustEl.appendChild(s);
}

// ── Buka / tutup buku ──────────────────────────────────────
function bukaBuku() {
    document.getElementById('book').classList.add('buka');
    setTimeout(() => {
        document.getElementById('appPage').classList.add('tampil');
        loadTasks();
    }, 600);
}

function tutupApp() {
    document.getElementById('appPage').classList.remove('tampil');
    setTimeout(() => {
        document.getElementById('book').classList.remove('buka');
    }, 300);
}

// ══════════════════════════════════════════════════════════════
//  FUNGSI TUGAS — sama persis seperti script asli
// ══════════════════════════════════════════════════════════════

async function loadTasks() {

    const res = await fetch('/tasks');
    const data = await res.json();

    const list = document.getElementById('taskList');
    const empty = document.getElementById('emptyState');

    list.innerHTML = '';

    if (data.length === 0) {
        empty.style.display = 'block';
        return;
    }

    empty.style.display = 'none';

    data.forEach((task, index) => {

        const li = document.createElement('li');
        li.setAttribute('data-num', index + 1);

        li.innerHTML = `
            <span class="teks ${task.done ? 'selesai' : ''}">
                ${task.text}
            </span>
            <div class="btn-group">
                <button onclick="toggleTask(${index})" title="Selesai">✓</button>
                <button onclick="deleteTask(${index})" title="Hapus">🗑</button>
            </div>
        `;

        list.appendChild(li);
    });
}

async function addTask() {

    const input = document.getElementById('taskInput');

    if (input.value.trim() === '') return;

    await fetch('/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input.value })
    });

    input.value = '';
    loadTasks();
}

async function deleteTask(index) {

    await fetch(`/delete/${index}`, {
        method: 'DELETE'
    });

    loadTasks();
}

async function toggleTask(index) {

    await fetch(`/toggle/${index}`, {
        method: 'POST'
    });

    loadTasks();
}

async function undoTask() {

    await fetch('/undo', {
        method: 'POST'
    });

    loadTasks();
}

async function redoTask() {

    await fetch('/redo', {
        method: 'POST'
    });

    loadTasks();
}