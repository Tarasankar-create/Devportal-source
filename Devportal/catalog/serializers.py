from rest_framework import serializers
from .models import Project, Environment, Deployment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields="__all__"

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Environment
        fields="__all__"

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Deployment
        fields="__all__"