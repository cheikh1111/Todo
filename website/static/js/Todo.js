let form = document.querySelector('form');
let todoInput = form.querySelector('input');
let addButton = form.querySelector('button');
let tasksDiv = document.querySelector('.tasks');
let tasks =  tasksDiv.querySelectorAll('.task');

sendRequest = (url,body,method,headers) => {
    return fetch(url, {
        method: method,
        body: body,
        headers: headers
    }).then(response => {
        if (!response.ok) console.error('Error sending request')
        else return response.json()
    })
};

deleteTodo = () => {
    let todoDiv = this.parentElement.parentElement;
    let todoId = todoDiv.getAttribute('todo_id');
    todoDiv.remove();

    sendRequest(`/delete-todo/${todoId}`,null,method='DELETE',headers={});
};


completeTodo = () => {
    let todoDiv = this.parentElement.parentElement;
    let todoId = todoDiv.getAttribute('todo_id');
    let todo = todoDiv.querySelector('p');
    todo.style.color = 'green';
    todo.style.textDecoration = 'underline';
    let requestBody = JSON.stringify({
        todo_id: todoId
    })
    sendRequest('/complete-todo',requestBody,method='PUT',headers={})
};


editTodo = () => {
    let todoDiv = this.parentElement.parentElement;
    let todo = todoDiv.querySelector('p').innerText;
    todoInput.value = todo;
};


addButton.onclick = () => {
    if (this.innerText === 'Add'){
        let todo = addInput.value;
        let requestBody = JSON.stringify({
            todo: todo
        });
        sendRequest('/add-todo',body=requestBody,method='POST',headers = {})
        .then(res => {
            todoId = res.todo_id;
            tasks.
        })
    } else if (this.innerText === 'Save'){

    }
}