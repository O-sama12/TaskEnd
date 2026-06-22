from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Task
# Create your views here.
def landing(request):
    return render(request, "HTMLs/index.html")
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        gender = request.POST.get("gender")
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return redirect("login")
    return render(request, "HTMLs/signup.html")
def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("tasks")

    return render(request, "HTMLs/login.html")
def forget_pass(request):
    return render(request, "HTMLs/forget_pass.html")
@login_required
def tasks(request):
    if request.method == "POST":
        title = request.POST["task_title"]

        Task.objects.create(
            title=title,
            owner=request.user
        )

    tasks = Task.objects.filter(
        owner=request.user
    )
    return render(request, "HTMLs/tasks.html",{"tasks": tasks})
@login_required
def complete_task(request, task_id):
    task = Task.objects.get(id = task_id, owner = request.user)
    task.completed = True
    task.save()
    return redirect("tasks")
@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id = task_id, owner = request.user)
    task.delete()
    return redirect("tasks")