let currentFilter = "all";

// =====================
// OPEN / CLOSE BOOK
// =====================

function openBook(){

    document.getElementById("coverPage").style.display = "none";

    document.getElementById("appPage").style.display = "flex";

    loadTasks();
}

function closeBook(){

    document.getElementById("appPage").style.display = "none";

    document.getElementById("coverPage").style.display = "flex";
}


// =====================
// LOAD TASKS
// =====================

async function loadTasks(){

    const res = await fetch("/tasks");

    const data = await res.json();

    const taskList =
        document.getElementById("taskList");

    const emptyState =
        document.getElementById("emptyState");

    const keyword =
        document.getElementById("searchInput")
        .value
        .toLowerCase();

    taskList.innerHTML = "";

    let count = 0;

    data.forEach((task,index)=>{

        // FILTER

        if(
            currentFilter === "done" &&
            !task.done
        ){
            return;
        }

        if(
            currentFilter === "undone" &&
            task.done
        ){
            return;
        }

        // SEARCH

        if(
            keyword &&
            !task.text
            .toLowerCase()
            .includes(keyword)
        ){
            return;
        }

        count++;

        const li =
            document.createElement("li");

        li.innerHTML = `

            <span class="
                task-text
                ${task.done ? "done" : ""}
            ">
                ${task.text}
            </span>

            <div class="action-buttons">

                <button
                    class="edit-btn"
                    onclick="editTask(${index})"
                >
                    ✏️
                </button>

                <button
                    class="done-btn"
                    onclick="toggleTask(${index})"
                >
                    ✓
                </button>

                <button
                    class="delete-btn"
                    onclick="deleteTask(${index})"
                >
                    🗑
                </button>

            </div>

        `;

        taskList.appendChild(li);
    });

    if(count === 0){

        emptyState.style.display = "block";

    }else{

        emptyState.style.display = "none";
    }
}


// =====================
// ADD TASK
// =====================

async function addTask(){

    const input =
        document.getElementById("taskInput");

    const text =
        input.value.trim();

    if(text === ""){

        alert("Tugas kosong!");

        return;
    }

    await fetch("/add",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            text:text
        })

    });

    input.value = "";

    loadTasks();
}


// =====================
// DELETE
// =====================

async function deleteTask(index){

    if(
        !confirm(
            "Yakin ingin menghapus tugas?"
        )
    ){
        return;
    }

    await fetch(
        `/delete/${index}`,
        {
            method:"DELETE"
        }
    );

    loadTasks();
}


// =====================
// TOGGLE DONE
// =====================

async function toggleTask(index){

    await fetch(

        `/toggle/${index}`,

        {
            method:"POST"
        }

    );

    loadTasks();
}


// =====================
// EDIT
// =====================

async function editTask(index){

    const res =
        await fetch("/tasks");

    const data =
        await res.json();

    const oldText =
        data[index].text;

    const newText =
        prompt(
            "Edit tugas:",
            oldText
        );

    if(
        newText === null
    ){
        return;
    }

    if(
        newText.trim() === ""
    ){
        alert(
            "Tugas tidak boleh kosong!"
        );

        return;
    }

    await fetch(

        `/edit/${index}`,

        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                text:newText
            })
        }
    );

    loadTasks();
}


// =====================
// FILTER
// =====================

function setFilter(type){

    currentFilter = type;

    loadTasks();
}


// =====================
// UNDO
// =====================

async function undoTask(){

    await fetch(

        "/undo",

        {
            method:"POST"
        }

    );

    loadTasks();
}


// =====================
// REDO
// =====================

async function redoTask(){

    await fetch(

        "/redo",

        {
            method:"POST"
        }

    );

    loadTasks();
}


// =====================
// START
// =====================

window.onload = function(){

    loadTasks();
};