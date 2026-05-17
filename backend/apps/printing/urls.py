from django.urls import path
from . import views

app_name = 'printing'

urlpatterns = [
    path('upload/', views.upload_stl, name='upload'),
    path('confirm/<int:pk>/', views.confirm_print, name='confirm'),
    path('my-uploads/', views.my_uploads, name='my_uploads'),
]
