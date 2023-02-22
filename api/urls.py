from django.urls import path
from .views import DocumentUploadView, DocumentListView, DocumentSearchView

urlpatterns = [
    path('documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    # path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/search/', DocumentSearchView.as_view(), name='document-search'),
]