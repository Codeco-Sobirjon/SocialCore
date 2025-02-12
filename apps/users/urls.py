from django.urls import path

from apps.users.views import (
    DemographicDataAPIView, DemographicDataDetailAPIView,
    MedicalHistoryAPIView, MedicalHistoryDetailAPIView,
    NotesAPIView, NotesDetailAPIView,
    InterestsAPIView, InterestsDetailAPIView,
    DiseaseHistoryDailyAPIView, DiseaseHistoryDailyDetailAPIView,
    MedicalIllnessAPIView
)

urlpatterns = [
    # Демографические данные
    path('demographics/', DemographicDataAPIView.as_view(), name='demographic-data-list'),
    path('demographics/<int:pk>/', DemographicDataDetailAPIView.as_view(), name='demographic-data-detail'),

    # Медицинская история
    path('medical-history/', MedicalHistoryAPIView.as_view(), name='medical-history-list'),
    path('medical-history/<int:pk>/', MedicalHistoryDetailAPIView.as_view(), name='medical-history-detail'),

    # Заметки
    path('notes/', NotesAPIView.as_view(), name='notes-list'),
    path('notes/<int:pk>/', NotesDetailAPIView.as_view(), name='notes-detail'),

    # Интересы
    path('interests/', InterestsAPIView.as_view(), name='interests-list'),
    path('interests/<int:pk>/', InterestsDetailAPIView.as_view(), name='interests-detail'),

    # Мои истории
    path('daily_history/', DiseaseHistoryDailyAPIView.as_view(), name='daily_history-list'),
    path('daily_history/<int:pk>/', DiseaseHistoryDailyDetailAPIView.as_view(), name='daily_history-detail'),

    path('medical/illness/', MedicalIllnessAPIView.as_view(), name='medical-illness')
]
