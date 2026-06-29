from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import IntegrityError
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from .models import Task
# Create your views here.
def landing(request):
    return render(request, "HTMLs/index.html")
def signup(request):
    if request.method == "POST":
        try:
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
        except IntegrityError:
            messages.error(request, "Username already exists")
            return redirect("signup")
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
    return render(request, "HTMLs/tasks.html",{"tasks": tasks, "now" : now()})
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
@login_required
def logout_view(request):
    logout(request)
    return redirect("landing")
class TaskListAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data)
    def post(self, request):
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status=400)
class TaskDetailAPIView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id = task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    def put(self, request, task_id):
        task = get_object_or_404(Task, id = task_id)
        serializer = TaskSerializer(task, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)
    def patch(self, request, task_id):
        task = get_object_or_404(Task, id = task_id)
        serializer = TaskSerializer(task, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)
    def delete(self, request, task_id):
        task = get_object_or_404(Task, id = task_id)
        task.delete()
        return Response(status = 204)