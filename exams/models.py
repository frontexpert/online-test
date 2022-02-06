from django.db import models
from django.contrib.auth.models import User
from admins.models import *

# Create your models here.
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    attempt_at = models.DateTimeField()
    correct_question_ids = models.CharField(max_length=255)
    complete_terminate = models.BooleanField(default=False)

class Process(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer_ids = models.CharField(max_length=255)