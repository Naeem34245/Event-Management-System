from django.urls import path
from . import views

urlpatterns = [
    path('', views.organizer_dashboard, name="organizer-dashboard"),
    path('create-event/', views.create_event, name='create-event'),
    path('update-event/<int:id>/', views.update_event, name='update-event'),
    path('delete-event/<int:id>/', views.delete_event, name='delete-event'),
]