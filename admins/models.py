from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)

class Section(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

class Question(models.Model):
    LEVEL = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    TYPE = ( 
        ('single', 'Single'),
        ('multiple', 'Multiple'),
    )
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    qlevel = models.CharField(max_length=100, choices=LEVEL, default='easy')
    answer_type = models.CharField(max_length=100, choices=TYPE, default='single')
    explanation = models.TextField(default='')
    path = models.CharField(max_length=255, default='')

class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct_type = models.BooleanField(default=False)

class Paper(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    time_limit = models.IntegerField(default=1)
    question_ids = models.CharField(max_length=255)

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)