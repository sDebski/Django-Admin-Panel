from django.contrib import admin
from core import models


@admin.register(models.Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Label)
class LabelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
