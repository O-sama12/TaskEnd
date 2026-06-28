from django.contrib import admin
from .models import Task
# Register your models here.
@admin.action(description="Mark selected tasks as completed")
def mark_completed(modeladmin, request, queryset):
    queryset.update(completed=True)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "owner",
        "priority",
        "completed",
        "deadline",
        "created_at",
    )

    search_fields = (
        "title",
        "owner__username",
    )

    list_filter = (
        "completed",
        "priority",
        "owner",
        "created_at",
    )

    ordering = ("completed", "-created_at",)

    list_per_page = 20

    date_hierarchy = "created_at"

    empty_value_display = "-"

    readonly_fields = (
        "created_at",
    )

    save_on_top = True

    actions = [mark_completed]


admin.site.site_header = "TaskEnd Administration"
admin.site.site_title = "TaskEnd Admin"
admin.site.index_title = "Welcome to TaskEnd Admin Portal"