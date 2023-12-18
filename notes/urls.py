from django.urls import path

from .views import home, edit, delete

urlpatterns = [
    path('', home, name='home'),
    path('edit/<int:note_id>/', edit, name='edit'),
    path('delete/<int:note_id>/', delete, name='delete')

]