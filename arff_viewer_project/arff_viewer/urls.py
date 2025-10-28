from django.urls import path
from . import views

app_name = 'arff_viewer'

urlpatterns = [
    path('', views.arff_upload_and_display, name='upload_display'),
]