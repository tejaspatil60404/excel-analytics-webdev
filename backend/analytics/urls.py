from django.urls import path
from .views import analyze_survey

urlpatterns = [
    path('analyze/<int:form_id>/', analyze_survey, name='analyze_survey'),
]
