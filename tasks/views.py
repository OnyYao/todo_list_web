"""
Views for the TODO list app.
"""

import json
from datetime import date
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Task


def _json_request(request):
    """Parse JSON body from request."""
    try:
        return json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return {}


@ensure_csrf_cookie
def index(request):
    """Serve the main app page."""
    if request.user.is_authenticated:
        return render(request, "tasks/app.html")
    return redirect("login")


def login_view(request):
    """Handle login."""
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        data = _json_request(request)
        username = data.get("username", "").strip()
        password = data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": True, "redirect": "/"})
        return JsonResponse({"success": False, "error": "Invalid username or password"}, status=400)
    return render(request, "tasks/login.html")


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        data = _json_request(request)
        username = data.get("username", "").strip()
        password = data.get("password", "")
        email = data.get("email", "").strip()
        if not username or not password:
            return JsonResponse({"success": False, "error": "Username and password required"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already taken"}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return JsonResponse({"success": True, "redirect": "/"})
    return render(request, "tasks/register.html")


def logout_view(request):
    """Handle logout."""
    logout(request)
    return redirect("login")


@login_required
@require_http_methods(["GET"])
def api_tasks(request):
    """List tasks for the current user. ?today=1 filters to today's tasks."""
    tasks = Task.objects.filter(user=request.user)
    if request.GET.get("today") == "1":
        tasks = tasks.filter(due_date=date.today())
    return JsonResponse({
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "due_date": t.due_date.isoformat(),
                "course": t.course,
                "completed": t.completed,
                "created_at": t.created_at.isoformat(),
            }
            for t in tasks
        ]
    })


@login_required
@require_http_methods(["POST"])
def api_task_create(request):
    """Create a new task."""
    data = _json_request(request)
    title = data.get("title", "").strip()
    if not title:
        return JsonResponse({"success": False, "error": "Title is required"}, status=400)
    due_date_str = data.get("due_date")
    if not due_date_str:
        return JsonResponse({"success": False, "error": "Due date is required"}, status=400)
    try:
        due_date = date.fromisoformat(due_date_str)
    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid due date format"}, status=400)
    task = Task.objects.create(
        user=request.user,
        title=title,
        description=data.get("description", ""),
        due_date=due_date,
        course=data.get("course", "").strip(),
    )
    return JsonResponse({
        "success": True,
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat(),
            "course": task.course,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
        },
    })


@login_required
@require_http_methods(["PUT", "PATCH"])
def api_task_update(request, task_id):
    """Update a task."""
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return JsonResponse({"success": False, "error": "Task not found"}, status=404)
    data = _json_request(request)
    if "title" in data and data["title"]:
        task.title = data["title"].strip()
    if "description" in data:
        task.description = data.get("description", "")
    if "due_date" in data:
        try:
            task.due_date = date.fromisoformat(data["due_date"])
        except (ValueError, TypeError):
            return JsonResponse({"success": False, "error": "Invalid due date"}, status=400)
    if "course" in data:
        task.course = data.get("course", "").strip()
    if "completed" in data:
        task.completed = bool(data["completed"])
    task.save()
    return JsonResponse({
        "success": True,
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat(),
            "course": task.course,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
        },
    })


@login_required
@require_http_methods(["DELETE"])
def api_task_delete(request, task_id):
    """Delete a task."""
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return JsonResponse({"success": False, "error": "Task not found"}, status=404)
    task.delete()
    return JsonResponse({"success": True})


@login_required
@require_http_methods(["GET"])
def api_today_count(request):
    """Return count of tasks due today (for morning reminder badge)."""
    count = Task.objects.filter(user=request.user, due_date=date.today(), completed=False).count()
    return JsonResponse({"count": count})
