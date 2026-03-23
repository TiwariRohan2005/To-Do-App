let todoListEl = document.getElementById("todoList");
let addBtn = document.getElementById("addBtn");
let inputEl = document.getElementById("todoInput");

let todos = [];

async function fetchTodos() {
  try {
    let res = await fetch("/todos");
    let data = await res.json();

    todos = data.map((t) => ({
      id: t[0],
      text: t[1],
      completed: t[2] === 1
    }));

    renderTodos();
  } catch (err) {
    console.error("Error fetching todos:", err);
  }
}

async function addTodo(text) {
  try {
    await fetch("/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: text })
    });

    fetchTodos();
  } catch (err) {
    console.error("Error adding todo:", err);
  }
}

async function deleteTodo(id) {
  try {
    await fetch(`/delete/${id}`, {
      method: "DELETE"
    });

    fetchTodos();
  } catch (err) {
    console.error("Error deleting todo:", err);
  }
}

async function toggleTodo(id) {
  try {
    await fetch(`/toggle/${id}`, {
      method: "PUT"
    });

    fetchTodos();
  } catch (err) {
    console.error("Error toggling todo:", err);
  }
}

function renderTodos() {
  todoListEl.innerHTML = "";

  todos.forEach((todo) => {
    let li = document.createElement("li");
    li.className = "todo-item-container";

    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "checkbox-input";
    checkbox.checked = todo.completed;

    checkbox.onclick = () => {
      toggleTodo(todo.id);
    };

    let labelContainer = document.createElement("div");
    labelContainer.className = "label-container";

    let label = document.createElement("label");
    label.className = "checkbox-label";
    label.textContent = todo.text;

    if (todo.completed) {
      label.classList.add("checked");
    }

    let deleteIcon = document.createElement("i");
    deleteIcon.className = "fa-solid fa-trash delete-icon";

    deleteIcon.onclick = () => {
      deleteTodo(todo.id);
    };

    labelContainer.appendChild(label);
    labelContainer.appendChild(deleteIcon);

    li.appendChild(checkbox);
    li.appendChild(labelContainer);

    todoListEl.appendChild(li);
  });
}

addBtn.onclick = () => {
  let text = inputEl.value.trim();

  if (text === "") {
    alert("Enter valid text");
    return;
  }

  addTodo(text);
  inputEl.value = "";
};

inputEl.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    addBtn.click();
  }
});

fetchTodos();