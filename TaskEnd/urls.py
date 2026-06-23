from django.urls import path, include
from .views import landing, signup, login_view, forget_pass, tasks, complete_task, delete_task, logout_view

urlpatterns = [
    path('', landing, name='landing'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('forget_pass/', forget_pass, name='forget_pass'),
    path('tasks/', tasks, name='tasks'),
    path('complete/<int:task_id>/', complete_task, name='complete_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('logout/', logout_view, name='logout'),
    path("accounts/", include("allauth.urls"))
]