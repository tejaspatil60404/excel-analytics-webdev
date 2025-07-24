from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import SurveyForm
from .serializers import SurveyFormSerializer, SurveyResponseSerializer, SurveyResponse

class SurveyFormCreateView(generics.CreateAPIView):
    queryset = SurveyForm.objects.all()
    serializer_class = SurveyFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserSurveyListView(generics.ListAPIView):
    serializer_class = SurveyFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SurveyForm.objects.filter(user=self.request.user)
    
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class SurveyResponseSubmitView(APIView):
    permission_classes = [permissions.AllowAny]  # or IsAuthenticated if private form

    def post(self, request, form_id):
        form = get_object_or_404(SurveyForm, id=form_id)
        serializer = SurveyResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(form=form)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurveyResponseListView(generics.ListAPIView):
    serializer_class = SurveyResponseSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only form owner can view

    def get_queryset(self):
        form_id = self.kwargs['form_id']
        form = get_object_or_404(SurveyForm, id=form_id, user=self.request.user)
        return SurveyResponse.objects.filter(form=form).order_by('-submitted_at')

class SurveyFormDetailView(generics.RetrieveAPIView):
    queryset = SurveyForm.objects.all()
    serializer_class = SurveyFormSerializer
    permission_classes = [permissions.AllowAny]  # ✅ Anyone can fetch form schema
    lookup_field = 'id'

class SurveyFormUpdateView(generics.UpdateAPIView):
    queryset = SurveyForm.objects.all()
    serializer_class = SurveyFormSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        # Only allow the form owner to update it
        return self.queryset.filter(user=self.request.user)

class SurveyFormDeleteView(generics.DestroyAPIView):
    queryset = SurveyForm.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
