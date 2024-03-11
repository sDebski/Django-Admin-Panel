from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from core import models
from django.db.models import Count


@admin.register(models.Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
    )
    list_editable = ("username",)
    ordering = ("username",)


@admin.register(models.Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "category",
        "tasks",
    )
    search_fields = ("name",)
    list_per_page = 5
    list_filter = ("category",)

    def tasks(self, obj):
        return obj.task_set.count()

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.annotate(tasks_count=Count("task"))

    tasks.order_admin_field = "tasks_count"


@admin.register(models.ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "status",
        "project",
        "assigned_to",
        "comments",
    )

    def comments(self, obj):
        return obj.comment_set.count()
    
    list_per_page = 5
    list_filter = ("labels",)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task",)

    