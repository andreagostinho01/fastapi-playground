from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import getpass

from server import startServer

# Setup
app = FastAPI()

class Todo(BaseModel):
  id: Optional[int]
  what: str
  completed: bool

todoList = []

# Routes
@app.get("/")
def welcome_message():
  return { "message": "Welcome, " + getpass.getuser() }

@app.get("/todos")
def get_all_todos():
  if (len(todoList) <= 0):
    return { "message": "Todo list is empty" }

  return { "todos": todoList }

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
  for todo in todoList:
    if (todo.id == todo_id):
      return { "todo": todo }

  return JSONResponse(
    status_code = 404,
    content = { "message": "Todo not found" }
  )

@app.post("/todos", status_code = 201)
def create_todo(newTodo: Todo):
  for todo in todoList:
    if (todo.id == newTodo.id):
      return JSONResponse(
        status_code = 400,
        content = { "message": "Id already exists in todo list" }
      )

  todoList.append(newTodo)
  return { "message": "Todo created!" }

@app.patch("/todos/{todo_id}")
def update_todo(todo_id: int, updateTodo: Todo):
  for todo in todoList:
    if (todo.id == todo_id):
      todo.what = updateTodo.what
      todo.completed = updateTodo.completed

      return { "todo": todo }

  return JSONResponse(
    status_code = 404,
    content = { "message": "Todo not found" }
  )

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
  for todo in todoList:
    if (todo.id == todo_id):
      todoList.remove(todo)
      return { "message": "Todo deleted!" }

  return JSONResponse(
    status_code = 404,
    content = { "message": "Todo not found" }
  )

# Start the server
startServer(app)
