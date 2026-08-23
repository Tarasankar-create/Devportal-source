from django.db import models

# track application repo
class Project(models.Model):
    name=models.CharField(max_length=100,unique=True)
    repo_url=models.URLField(blank=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

#Deploy target for project
class Environment(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="environments")
    name=models.CharField(max_length=50) #dev,staging,prod
    namespace=models.CharField(max_length=100,blank=True)

    class Meta:
        unique_together=("project","name")
    def __str__(self):
        return f"{self.project.name}/{self.name}"

#Deployment record per environment
class Deployment(models.Model):
    STATUS_CHOICES=[
        ("pending","pending"),
        ("building","building"),
        ("deployed","deployed"),
        ("failed","failed"),
        ("syncing","syncing"),
    ]
    environment=models.ForeignKey(Environment,on_delete=models.CASCADE,related_name="deployments")
    image_tag=models.CharField(max_length=100,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")
    triggered_by=models.CharField(max_length=100,blank=True)
    last_synced_at=models.DateTimeField(null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-updated_at"]

    def __str__(self):
        return f"{self.environment}-{self.status}({self.image_tag})"
