from django.db import models

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    join_date = models.DateField()

    def __str__(self):
        return self.name


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("P", "Present"),
        ("A", "Absent"),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)


    def __str__(self):
        return self.date
    

from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()

    def __str__(self):
        return self.username


TASK_STATUS_CHOICES = [
    ("PENDING", "Pending"),
    ("IN_PROGRESS", "In Progress"),
    ("COMPLETED", "Completed"),
]

class Task(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


    def serialize(self):    
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "status": self.status,
                "is_completed": self.is_completed,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "user": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name,
                    "dob": self.user.dob,
                },
            }