from django.urls import path
from .views import SurveyFormCreateView, UserSurveyListView
from .views import SurveyResponseSubmitView
from .views import SurveyResponseListView
from .views import SurveyFormDetailView
from .views import SurveyFormUpdateView
from .views import SurveyFormDeleteView

urlpatterns = [
    path('create/', SurveyFormCreateView.as_view(), name='create-survey'),
    path('', UserSurveyListView.as_view(), name='user-surveys'),
    path('<int:form_id>/response/', SurveyResponseSubmitView.as_view(), name='submit-response'),
    path('<int:form_id>/responses/', SurveyResponseListView.as_view(), name='list-responses'),
    path('<int:id>/', SurveyFormDetailView.as_view(), name='survey-detail'),
    path('<int:pk>/update/', SurveyFormUpdateView.as_view(), name='form-update'),
    path('<int:pk>/delete/', SurveyFormDeleteView.as_view(), name='form-delete'),
]
