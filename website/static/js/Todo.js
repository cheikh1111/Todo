let form = document.querySelector("form");
let todoInput = form.querySelector("input");
let addButton = form.getElementById("submit");
let tasksDiv = document.querySelector(".tasks");
let tasks = tasksDiv.querySelectorAll(".task");

sendRequest = async (url, body, method, headers, ...other) => {
    return await fetch(url, {
        method: method,
        body: body,
        headers: headers,
    }).then((response) => {
        if (!response.ok) console.error("Error sending request");
        else return response.json();
    });
};

deleteTodo = (button) => {
    let todoDiv = button.parentElement.parentElement;
    let todoId = todoDiv.getAttribute("todo_id");
    todoDiv.remove();

    sendRequest(
        `/delete-todo/${todoId}`,
        null,
        (method = "DELETE"),
        (headers = {})
    );
};

completeTodo = (button) => {
    let todoDiv = button.parentElement.parentElement;
    let todoId = todoDiv.getAttribute("todo_id");
    let todo = todoDiv.querySelector("p");
    todo.style.color = "#30ba4e";
    todo.style.textDecoration = "line-through";
    let requestBody = JSON.stringify({
        todo_id: todoId,
    });
    sendRequest(
        "/complete-todo",
        requestBody,
        (method = "PUT"),
        (headers = {})
    );
};

editTodo = (button) => {
    let todoDiv = button.parentElement.parentElement;
    let todo = todoDiv.querySelector("p").innerText;
    todoInput.value = todo;
    todoInput.setAttribute(
        "current_todo_id",
        todoDiv.getAttribute("current_todo_id")
    );
    validateButtons();
};

addButton.onclick = () => {
    if (button.innerText === "Add") {
        let todo = addInput.value;
        let requestBody = JSON.stringify({
            todo: todo,
        });
        sendRequest(
            "/add-todo",
            (body = requestBody),
            (method = "POST"),
            (headers = {})
        ).then((res) => {
            todoId = res.todo_id;
            let todoHtml = `<div todo_id=${todoId} class="task">
                                <p>${todo}</p>
                                <div class="controls">
                                    <button class="complete">Completed</button>
                                    <button class="edit">Edit</button>
                                    <button class="delete">Delete</button>
                                </div>             
                            </div>`;
            tasks.insertAdjacentHTML("afterbegin", todoHtml);
        });
    } else if (button.innerText === "Save") {
        let todo = addInput.value;
        let todoId = addInput.getAttribute("current_todo_id");
        let requestBody = JSON.stringify({
            todo: todo,
            todo_id: todoId,
        });

        sendRequest(
            "/edit-todo",
            (body = requestBody),
            (method = "PUT"),
            (headers = {})
        ).then((res) => {
            let task = tasks.querySelector(`.task[todo_id = "${todoId}"]`);
            task.innerHtml = `<div todo_id=${todoId} class="task">
                                <p>${todo}</p>
                                <div class="controls">
                                    <button class="complete">Completed</button>
                                    <button class="edit">Edit</button>
                                    <button class="delete">Delete</button>
                                </div>             
                            </div>`;
        });
    }
    todoInput.value = "";
    validateButtons();
};

let validateButtons = () => {
    let deleteButtons = document.querySelectorAll(".task .controls .delete");
    let editButtons = document.querySelectorAll(".task .controls .edit");
    let completeButtons = document.querySelectorAll(
        ".task .controls .complete"
    );

    for (button of deleteButtons) {
        button.onclick = () => deleteTodo(button);
    }

    for (button of completeButtons) {
        button.onclick = () => completeTodo(button);
    }

    for (button of editButtons) {
        button.onclick = () => editTodo(button);
    }
};

validateButtons();
