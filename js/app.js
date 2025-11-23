
const API_URL = 'http://localhost:8000'; 
let tasks = []; 
let filterSelect; 

function sanitizeHtml(str = '') {
    return String(str).replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]));
}

async function fetchTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        if (!response.ok) {
            throw new Error(`Błąd HTTP! Status: ${response.status}`);
        }
        
        tasks = await response.json(); 
        const currentFilter = filterSelect ? filterSelect.value : 'all';
        renderTasks(currentFilter);
        
    } catch (error) {
        console.error('Błąd podczas pobierania zadań (GET):', error);
        document.getElementById('task-list').innerHTML = '<li style="color:red;">Nie udało się załadować zadań z API.</li>';
    }
}

async function addTaskFromForm(e) {
    if (e) e.preventDefault();
    const taskInput = document.getElementById('task-input');
    const assigneeInput = document.getElementById('assignee-input');
    
    const name = taskInput.value.trim();
    const assignee = assigneeInput.value.trim();

    if (!name) return;

    const taskData = { 
        title: name,
        description: assignee 
    };

    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });

        if (response.status !== 201) {
            throw new Error(`Błąd POST: ${response.status}`);
        }
        
        taskInput.value = '';
        assigneeInput.value = '';
        fetchTasks();
        
    } catch (error) {
        console.error('Błąd POST:', error);
        alert('Nie udało się dodać zadania.');
    }
}

async function toggleTaskById(id) {
    const task = tasks.find(x => x.id == id);
    if (!task) return; 

    const newCompletedStatus = !task.completed;
    const updateData = { completed: newCompletedStatus };

    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        });

        if (!response.ok) {
            throw new Error(`Błąd PUT: ${response.status}`);
        }

        fetchTasks(); 
        
    } catch (error) {
        console.error('Błąd PUT:', error);
        alert('Nie udało się zaktualizować statusu.');
    }
}

async function deleteTaskById(id) {
    if (!confirm("Czy na pewno chcesz usunąć to zadanie?")) return;
            
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok && response.status !== 204) {
            throw new Error(`Błąd DELETE: ${response.status}`);
        }
        
        fetchTasks();
    } catch (error) {
        console.error('Błąd DELETE:', error);
        alert('Błąd usuwania zadania.');
    }
}

function renderTasks(filter = 'all') {
    const taskList = document.getElementById('task-list');
    
    const filtered = tasks.filter(t => {
        if (filter === 'active') return !t.completed;
        if (filter === 'completed') return t.completed;
        return true;
    });

    taskList.innerHTML = '';

    filtered.forEach(task => {
        const li = document.createElement('li');
        li.className = 'task-item collection-item' + (task.completed ? ' completed' : '');
        li.dataset.id = task.id;

        li.innerHTML = `
            <label style="display:flex;align-items:center;width:100%">
                <input type="checkbox" class="task-toggle" ${task.completed ? 'checked' : ''} />
                <span style="flex:1;margin-left:10px">
                    <strong>${sanitizeHtml(task.title)}</strong>
                    ${task.description ? ` - <em>${sanitizeHtml(task.description)}</em>` : ''}
                </span>
                <div>
                    <button class="btn delete-btn red">Usuń</button>
                </div>
            </label>
        `;

        taskList.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', () => {
 
    filterSelect = document.getElementById('filter-select');
    totalTasksElement = document.getElementById('total-tasks');
    completedTasksElement = document.getElementById('completed-tasks');
    activeTasksElement = document.getElementById('active-tasks');
    progressBar = document.getElementById('progress-bar');
    progressBarContainer = document.getElementById('progress-bar-container'); // Zdefiniuj ten element

    if (!document.getElementById('title-input') || !document.getElementById('description-input') || !document.getElementById('task-list') || !filterSelect || !totalTasksElement) {
        console.error('Krytyczny błąd: Brak wymaganych elementów DOM. Sprawdź ID w HTML.');
        document.querySelector('.container').innerHTML = '<h2 style="color:red; text-align:center;">Błąd ładowania aplikacji.</h2>';
        return;
    }

let totalTasksElement, completedTasksElement, activeTasksElement, progressBar, progressBarContainer; 

    taskList.addEventListener('click', (ev) => {
        const li = ev.target.closest('li');
        if (!li) return;
        const id = li.dataset.id;
        
        if (ev.target.classList.contains('delete-btn')) {
            deleteTaskById(id);
            return;
        }
    });

    taskList.addEventListener('change', (ev) => {
        const li = ev.target.closest('li');
        if (!li) return;
        if (ev.target.classList.contains('task-toggle')) {
            toggleTaskById(li.dataset.id);
        }
    });

    if (taskForm) {
        taskForm.addEventListener('submit', addTaskFromForm);
    } else if (document.getElementById('addTaskButton')) { 
        document.getElementById('addTaskButton').addEventListener('click', addTaskFromForm);
    }

    if (filterSelect) {
        filterSelect.addEventListener('change', (e) => renderTasks(e.target.value));
    }
    
    fetchTasks();
});