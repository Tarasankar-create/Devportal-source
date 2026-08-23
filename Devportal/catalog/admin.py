from django.contrib import admin
from .models import Project,Environment,Deployment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=("name","repo_url","created_at")

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display=("project","name","namespace")

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display=("environment","status","image_tag","triggered_by","updated_at")