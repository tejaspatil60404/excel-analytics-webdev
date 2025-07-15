from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class SurveyForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    schema = models.JSONField()  # structure of form (question list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class SurveyResponse(models.Model):
    form = models.ForeignKey(SurveyForm, on_delete=models.CASCADE, related_name='responses')
    response = models.JSONField()  # user answers
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.form.title} at {self.submitted_at}"

