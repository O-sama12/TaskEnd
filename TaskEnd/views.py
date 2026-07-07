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
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django_ratelimit.exceptions import Ratelimited
# Create your views here.
def landing(request):
    return render(request, "HTMLs/index.html")
@ratelimit(key="ip", rate="3/m", method="POST", block=True)
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
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
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
@ratelimit(key="ip", rate="3/h", method="POST", block=True)
def forget_pass(request):
    return render(request, "HTMLs/forget_pass.html")
@login_required
@ratelimit(key="user_or_ip", rate="30/m", method="POST", block=True)
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
@ratelimit(key="user_or_ip", rate="60/m", block=True)
@login_required
def complete_task(request, task_id):
    task = Task.objects.get(id = task_id, owner = request.user)
    task.completed = True
    task.save()
    return redirect("tasks")
@ratelimit(key="user_or_ip", rate="60/m", block=True)
@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id = task_id, owner = request.user)
    task.delete()
    return redirect("tasks")
@ratelimit(key="user_or_ip", rate="60/m", block=True)
@login_required
def logout_view(request):
    logout(request)
    return redirect("landing")
@method_decorator(
    ratelimit(key="user_or_ip", rate="120/m", block=True),
    name="dispatch",
)
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
@method_decorator(
    ratelimit(key="user_or_ip", rate="120/m", block=True),
    name="dispatch",
)
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
def custom_403(request, exception):
    if isinstance(exception, Ratelimited):
        return HttpResponse(
            "<h1>429 Too Many Requests</h1>"
            "<p>Please wait a while before trying again.</p>",
            status=429,
        )

    return HttpResponse(
        "<h1>403 Forbidden</h1>"
        "<p>You don't have permission to access this resource.</p>",
        status=403,
    )