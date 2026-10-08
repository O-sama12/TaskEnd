from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', include('TaskEnd.urls')),

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="HTMLs/forget_pass_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="HTMLs/pass_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="HTMLs/pass_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="HTMLs/forget_pass.html",
            email_template_name="HTMLs/pass_reset_email.txt",
            html_email_template_name="HTMLs/pass_reset_email.html",
            subject_template_name="HTMLs/pass_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="HTMLs/pass_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]
handler403 = "TaskEnd.views.custom_403"