from . import views
from django.urls import path

urlpatterns = [
    path('', views.translate_View, name='translate_view'),
]
