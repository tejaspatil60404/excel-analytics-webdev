from rest_framework import serializers
from .models import SurveyForm

class SurveyFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyForm
        fields = ['id', 'title', 'description', 'schema', 'created_at']
        read_only_fields = ['id', 'created_at']

from .models import SurveyResponse

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['id', 'form', 'response', 'submitted_at']
        read_only_fields = ['id', 'form', 'submitted_at']
