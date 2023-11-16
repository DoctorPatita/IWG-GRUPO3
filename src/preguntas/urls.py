from django.urls import path
from . import views

app_name = 'preguntas'  # Opcional, pero puede ayudar a evitar conflictos de nombres

urlpatterns = [
    path('lista_preguntas/', views.lista_preguntas, name='lista_preguntas'),
    path('pregunta/<int:pregunta_id>/', views.detalle_pregunta, name='detalle_pregunta'),
    path('hacer_pregunta/', views.hacer_pregunta, name='hacer_pregunta'),
    path('pregunta/<int:pregunta_id>/responder/', views.responder_pregunta, name='responder_pregunta'),
    path('pregunta/<int:pregunta_id>/respuesta/<int:respuesta_id>/destacar/', views.destacar_respuesta, name='destacar_respuesta'),
]