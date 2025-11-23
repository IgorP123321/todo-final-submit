from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime, timezone

TASKS_FILE = "tasks.json"
app = FastAPI()

# KONFIGURACJA CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELE DANYCH
class TaskIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# FUNKCJE PLIKU JSON
def read_tasks() -> List[Dict[str, Any]]:
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            # Gwarantujemy, że zwracamy listę
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []

def write_tasks(tasks: List[Dict[str, Any]]):
    """Atomowy zapis danych, odporny na uszkodzenia i blokady pliku."""
    temp_file = TASKS_FILE + ".tmp"
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
        
        # Atomowa zamiana pliku
        os.replace(temp_file, TASKS_FILE) 
    except Exception as e:
        print(f"CRITICAL I/O ERROR: Failed to save {TASKS_FILE}. {e}")
        # Błąd 500 w przypadku krytycznej awarii zapisu
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server failed to save data due to system lock.")


def get_next_id(tasks: List[Dict[str, Any]]) -> int:
    if not tasks:
        return 1
    max_id = max(task.get("id", 0) for task in tasks)
    return max_id + 1

# ENDPOINTY
@app.get("/health")
def get_health():
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {"status": "OK", "timestamp": now_iso}

@app.get("/tasks", response_model=List[Dict[str, Any]])
def get_all_tasks():
    return read_tasks()

@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
def create_task(task_in: TaskIn):
    # BLĄD 400: Jeśli tytuł jest pusty przy tworzeniu zadania
    if not task_in.title: 
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, 
             detail="Title is required"
         )

    tasks = read_tasks()
    new_id = get_next_id(tasks)
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    new_task = {
        "id": new_id,
        "title": task_in.title,
        "description": task_in.description,
        "completed": False,
        "createdAt": now_iso
    }
    
    tasks.append(new_task)
    write_tasks(tasks)
    return new_task

@app.put("/tasks/{task_id}", response_model=Dict[str, Any])
def update_task(task_id: int, task_in: TaskIn):
    tasks = read_tasks()
    
    try:
        task_index = next(i for i, task in enumerate(tasks) if task["id"] == task_id)
    except StopIteration:
        # BŁĄD 404: Jeśli zadanie do modyfikacji nie istnieje
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"error": "Task not found", "id": task_id}
        )

    task_to_update = tasks[task_index]
    
    if task_in.title is not None:
        task_to_update["title"] = task_in.title
    if task_in.description is not None:
        task_to_update["description"] = task_in.description
    if task_in.completed is not None:
        task_to_update["completed"] = task_in.completed
        
    task_to_update["updatedAt"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    tasks[task_index] = task_to_update
    write_tasks(tasks)
    return task_to_update

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    tasks = read_tasks()
    original_len = len(tasks)
    tasks[:] = [task for task in tasks if task["id"] != task_id] 
    
    if len(tasks) == original_len:
        # BŁĄD 404: Jeśli zadanie do usunięcia nie zostało znalezione
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"error": "Task not found", "id": task_id}
        )

    write_tasks(tasks)
    return