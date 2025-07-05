from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):

    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    class Role(models.TextChoices):

        COMPANY_X_ADMIN = "COMPANY_X_ADMIN", "Company X Admin"
        COMPANY_X_EMPLOYEE = "COMPANY_X_EMPLOYEE", "Company X Employee"
        ORG_MANAGER = "ORG_MANAGER", "Organization Manager"
        ORG_WORKER = "ORG_WORKER", "Organization Worker"
        # ORG_VIEWER = "ORG_VIEWER", "Organization Viewer"

    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    role = models.CharField(max_length=50, choices=Role.choices)


class HmiGroup(models.Model):

    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="groups")


    class Meta:
        
        unique_together = ('organization', 'name')

    def __str__(self):
        return f"{self.name} ({self.organization.name})"
    

class HMI(models.Model):
    name = models.CharField(max_length=255)

 
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="hmis")

   
    groups = models.ManyToManyField(HmiGroup, related_name="hmis", blank=True)

    assigned_workers = models.ManyToManyField(User, related_name="assigned_hmis", blank=True)

    def __str__(self):
        return self.name
