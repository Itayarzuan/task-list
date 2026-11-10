from fastapi import FastAPI, HTTPException, Query
from typing import Optional

app = FastAPI()

tasks = []
counter = 1
VALID_PRIORITIES = {"low", "medium", "high"}

@app.get("/tasks")
def get_tasks(priority: Optional[str] = Query(None)):
    if priority:
        if priority not in VALID_PRIORITIES:
            raise HTTPException(status_code=400, detail="Invalid priority value. Must be low, medium, or high.")
        return [task for task in tasks if task.get("priority") == priority]
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: dict):
    global counter
    priority = task.get("priority")
    
    if not priority:
        raise HTTPException(status_code=400, detail="Field 'priority' is required")
    if priority not in VALID_PRIORITIES:
        raise HTTPException(status_code=400, detail="Invalid priority value. Must be low, medium, or high.")
        
    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
