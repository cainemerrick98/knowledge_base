from django.urls import path

from . import views

urlpatterns = [
    path("query", views.QueryDocumentView.as_view(), name='query'),
    path("upload", views.UploadDocumentView.as_view(), name='upload'),
    path("vote", views.VoteDocumentView.as_view(), name='vote')
]