from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')

    def __str__(self):
        return f"{self.subject} by {self.user.name}"
