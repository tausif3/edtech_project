from django.db import models
from django.contrib.auth.models import AbstractUser


# extending default django user model
class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    educator = models.BooleanField(default=False)
    student = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class StudentInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_class = models.IntegerField(blank=True)

    def __str__(self):
        return "student :%s", self.user


class EducatorInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    educator_qualifications = models.CharField(max_length=500, blank=True)
    educator_mobile_number = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return "educator :%s", self.user

