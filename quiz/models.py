# Create your models here.

from django.db import models
from django.conf import settings

class Subject(models.Model):
    title = models.CharField(max_length=120)
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Question(models.Model):
    MCQ = 'mcq'
    FIB = 'fib'
    QTYPE_CHOICES = [
        (MCQ, 'Multiple Choice'),
        (FIB, 'Fill in the blank'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    qtype = models.CharField(max_length=10, choices=QTYPE_CHOICES, default=MCQ)
    difficulty = models.IntegerField(default=1)
    choices = models.JSONField(blank=True, null=True)   # requires Postgres
    correct_answer = models.TextField()

    def __str__(self):
        return f"{self.subject.title} - {self.text[:60]}"


class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    total_questions = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    score = models.FloatField(null=True, blank=True)
    details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject.title} - {self.score}"
