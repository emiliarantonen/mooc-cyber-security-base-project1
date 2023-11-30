from django.urls import path

from .views import home, edit

urlpatterns = [
    path('', home, name='home'),
    path('edit/<int:note_id>/', edit, name='edit')
]