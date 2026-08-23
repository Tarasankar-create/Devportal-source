from django.shortcuts import render
from rest_framework import viewsets
from .models import Project, Environment, Deployment
from .serializers import ProjectSerializer, EnvironmentSerializer, DeploymentSerializer
from django.shortcuts import render

class ProjectViewSet(viewsets.ModelViewSet):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer

class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset=Environment.objects.all()
    serializer_class=EnvironmentSerializer

class DeploymentViewSet(viewsets.ModelViewSet):
    queryset=Deployment.objects.all()
    serializer_class=DeploymentSerializer

def dashboard(request):
    return render(request, 'dashboard.html')
