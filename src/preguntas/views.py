from django.shortcuts import render, redirect
from preguntas.models import Pregunta, Respuesta
from .forms import PreguntaForm


def lista_preguntas(request):
    preguntas = Pregunta.objects.all()  # aca estan todas las preguntas
    return render(request, 'preguntas/lista_preguntas.html', {'preguntas': preguntas})

def detalle_pregunta(request, pregunta_id):
    pregunta = Pregunta.objects.get(pk=pregunta_id)
    return render(request, 'preguntas/detalle_pregunta.html', {'pregunta': pregunta})

def hacer_pregunta(request):
    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            nueva_pregunta = form.save(commit=False)
            nueva_pregunta.autor = request.user  # asigna el autor actual
            nueva_pregunta.save()
            return redirect('lista_preguntas')  # redirige a la lista de preguntas
    else:
        form = PreguntaForm()
    
    return render(request, 'preguntas/hacer_pregunta.html', {'form': form})








