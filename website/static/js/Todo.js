function deleteTodo(todo_id) {
  fetch(`/delete-todo?todo_id=${todo_id}`, {
    method: 'GET',
  })
  .then((response) => {
    if (response.ok) {
      // Handle successful deletion
      window.location.href = '/';
    } else {
      // Handle unsuccessful deletion
      console.error('Failed to delete todo item.');
    }
  })
  .catch((error) => {
    console.error('An error occurred while deleting the todo item:', error);
  });
}
