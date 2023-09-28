from django.shortcuts import render
from preguntas.models import Pregunta, Respuesta

def lista_preguntas(request):
    preguntas = Pregunta.objects.all()  # Aca estan todas las preguntas
    return render(request, 'preguntas/lista_preguntas.html', {'preguntas': preguntas})
