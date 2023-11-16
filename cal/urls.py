from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('calendario/', views.CalendarView.as_view(), name='calendario'),
    path('evento/nuevo/', views.event, name='event_new'),
    path('evento/editar/<int:event_id>/', views.event, name='event_edit'),
]
