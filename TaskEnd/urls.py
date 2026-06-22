from django.urls import path
from .views import landing, signup, login_view, forget_pass, tasks

urlpatterns = [
    path('', landing, name='landing'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('forget_pass/', forget_pass, name="forget_pass"),
    path('tasks/', tasks, name="tasks")
]