/**
 * CMU Todo - Multiuser TODO list app
 */

const API = {
    tasks: () => fetch('/api/tasks/').then(r => r.json()),
    tasksToday: () => fetch('/api/tasks/?today=1').then(r => r.json()),
    todayCount: () => fetch('/api/tasks/today-count/').then(r => r.json()),
    create: (data) => fetch('/api/tasks/create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
        body: JSON.stringify(data)
    }).then(r => r.json()),
    update: (id, data) => fetch(`/api/tasks/${id}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
        body: JSON.stringify(data)
    }).then(r => r.json()),
    delete: (id) => fetch(`/api/tasks/${id}/delete/`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': getCsrfToken() }
    }).then(r => r.json())
};

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

const todayList = document.getElementById('today-list');
const todayEmpty = document.getElementById('today-empty');
const taskList = document.getElementById('task-list');
const taskForm = document.getElementById('task-form');
const btnAdd = document.getElementById('btn-add');
const btnCancel = document.getElementById('btn-cancel');
const filterBtns = document.querySelectorAll('.filter-btn');
const reminderHeader = document.querySelector('.reminder-header h2');
const taskFormLabel = document.getElementById('task-form-label');
const taskFormSubmit = document.getElementById('task-form-submit');

let allTasks = [];
let currentFilter = 'all';
let editingTaskId = null;

function formatDate(iso) {
    const d = new Date(iso);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    d.setHours(0, 0, 0, 0);
    if (d.getTime() === today.getTime()) return 'Today';
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    if (d.getTime() === tomorrow.getTime()) return 'Tomorrow';
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function isToday(iso) {
    const d = new Date(iso);
    const today = new Date();
    return d.toDateString() === today.toDateString();
}

function renderTaskItem(task, container) {
    if (!container) return;
    const li = document.createElement('li');
    li.className = 'task-item' + (task.completed ? ' completed' : '');
    li.dataset.id = task.id;

    const dueClass = isToday(task.due_date) ? 'today' : '';
    li.innerHTML = `
        <input type="checkbox" class="task-check" ${task.completed ? 'checked' : ''}>
        <div class="task-content">
            <div class="task-title">${escapeHtml(task.title)}</div>
            ${task.description ? `<div class="task-desc">${escapeHtml(task.description)}</div>` : ''}
            <div class="task-meta">
                ${task.course ? `<span class="task-course">${escapeHtml(task.course)}</span>` : ''}
                <span class="task-due ${dueClass}">${formatDate(task.due_date)}</span>
            </div>
        </div>
        <div class="task-actions">
            <button type="button" class="btn-edit">Edit</button>
            <button type="button" class="btn-delete">Delete</button>
        </div>
    `;

    const checkEl = li.querySelector('.task-check');
    const editBtn = li.querySelector('.btn-edit');
    const deleteBtn = li.querySelector('.btn-delete');
    if (checkEl) checkEl.addEventListener('change', () => toggleComplete(task.id));
    if (editBtn) editBtn.addEventListener('click', () => beginEdit(task));
    if (deleteBtn) deleteBtn.addEventListener('click', () => deleteTask(task.id));

    container.appendChild(li);
}

function escapeHtml(s) {
    const div = document.createElement('div');
    div.textContent = s;
    return div.innerHTML;
}

function setTaskFormMode(isEdit) {
    if (taskFormLabel) taskFormLabel.textContent = isEdit ? 'Edit task' : 'New task';
    if (taskFormSubmit) taskFormSubmit.textContent = isEdit ? 'Save changes' : 'Add task';
}

function resetTaskForm() {
    if (!taskForm) return;
    editingTaskId = null;
    taskForm.reset();
    taskForm.classList.add('hidden');
    setTaskFormMode(false);
}

function beginEdit(task) {
    if (!taskForm) return;
    editingTaskId = task.id;
    taskForm.classList.remove('hidden');
    setTaskFormMode(true);
    const titleEl = taskForm.querySelector('[name=title]');
    const descEl = taskForm.querySelector('[name=description]');
    const dueEl = taskForm.querySelector('[name=due_date]');
    const courseEl = taskForm.querySelector('[name=course]');
    if (titleEl) titleEl.value = task.title || '';
    if (descEl) descEl.value = task.description || '';
    if (dueEl) dueEl.value = task.due_date || '';
    if (courseEl) courseEl.value = task.course || '';
    taskForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function updateReminderHeader(count) {
    if (reminderHeader) {
        reminderHeader.textContent = count > 0
            ? `Good morning! You have ${count} task(s) due today`
            : "Good morning! Here's what's due today";
    }
}

function renderTodayTasks() {
    if (!todayList || !todayEmpty) return;
    todayList.innerHTML = '';
    const todayTasks = allTasks.filter(t => isToday(t.due_date) && !t.completed);
    if (todayTasks.length === 0) {
        todayEmpty.classList.remove('hidden');
    } else {
        todayEmpty.classList.add('hidden');
        todayTasks.forEach(t => renderTaskItem(t, todayList));
    }
}

function filterTasks() {
    if (!taskList) return;
    const now = new Date();
    now.setHours(0, 0, 0, 0);

    let filtered = allTasks;
    if (currentFilter === 'today') {
        filtered = allTasks.filter(t => isToday(t.due_date));
    } else if (currentFilter === 'upcoming') {
        filtered = allTasks.filter(t => new Date(t.due_date) >= now && !t.completed);
    }

    taskList.innerHTML = '';
    filtered.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
    filtered.forEach(t => renderTaskItem(t, taskList));
}

async function loadTasks() {
    try {
        const data = await API.tasks();
        allTasks = data.tasks || [];
        const todayCountData = await API.todayCount();
        const count = todayCountData?.count ?? allTasks.filter(t => isToday(t.due_date) && !t.completed).length;
        updateReminderHeader(count);
        renderTodayTasks();
        filterTasks();
    } catch (e) {
        console.error('Failed to load tasks:', e);
    }
}

async function toggleComplete(id) {
    const task = allTasks.find(t => t.id === id);
    if (!task) return;
    try {
        const res = await API.update(id, { completed: !task.completed });
        const data = res && typeof res === 'object' ? res : {};
        if (data.success) {
            task.completed = data.task?.completed ?? !task.completed;
            renderTodayTasks();
            filterTasks();
        }
    } catch (e) {
        console.error('Failed to update task:', e);
    }
}

async function deleteTask(id) {
    try {
        const res = await API.delete(id);
        const data = res && typeof res === 'object' ? res : {};
        if (data.success) {
            allTasks = allTasks.filter(t => t.id !== id);
            renderTodayTasks();
            filterTasks();
        }
    } catch (e) {
        console.error('Failed to delete task:', e);
    }
}

if (btnAdd && taskForm) {
    btnAdd.addEventListener('click', () => {
        editingTaskId = null;
        setTaskFormMode(false);
        taskForm.reset();
        taskForm.classList.remove('hidden');
        const today = new Date().toISOString().slice(0, 10);
        const dueInput = taskForm.querySelector('[name=due_date]');
        if (dueInput) dueInput.value = today;
    });
}

if (btnCancel && taskForm) {
    btnCancel.addEventListener('click', () => resetTaskForm());
}

if (taskForm) {
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData(taskForm);
        const data = {
            title: fd.get('title'),
            description: fd.get('description') || '',
            due_date: fd.get('due_date'),
            course: fd.get('course') || ''
        };
        try {
            if (editingTaskId != null) {
                const res = await API.update(editingTaskId, data);
                const result = res && typeof res === 'object' ? res : {};
                if (result.success && result.task) {
                    const i = allTasks.findIndex(t => t.id === editingTaskId);
                    if (i !== -1) allTasks[i] = result.task;
                    renderTodayTasks();
                    filterTasks();
                    resetTaskForm();
                } else {
                    alert(result.error || 'Failed to update task');
                }
            } else {
                const res = await API.create(data);
                const result = res && typeof res === 'object' ? res : {};
                if (result.success) {
                    allTasks.push(result.task);
                    renderTodayTasks();
                    filterTasks();
                    resetTaskForm();
                } else {
                    alert(result.error || 'Failed to add task');
                }
            }
        } catch (err) {
            alert('Network error. Please try again.');
        }
    });
}

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter || 'all';
        filterTasks();
    });
});

if (todayList && taskList) {
    loadTasks();
}
