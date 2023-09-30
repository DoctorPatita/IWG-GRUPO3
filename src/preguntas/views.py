from django.shortcuts import render, redirect
from preguntas.models import Pregunta, Respuesta
from .forms import PreguntaForm, RespuestaForm


def lista_preguntas(request):
    preguntas = Pregunta.objects.all()  # aca estan todas las preguntas
    return render(request, 'preguntas/lista_preguntas.html', {'preguntas': preguntas})

def detalle_pregunta(request, pregunta_id):
    pregunta = Pregunta.objects.get(pk=pregunta_id)

# Verifica si se ha enviado un formulario de respuesta
    if request.method == 'POST':
        respuesta_form = RespuestaForm(request.POST)
        if respuesta_form.is_valid():
            # Procesa y guarda la respuesta aquí
            # Se asigna la pregunta y el autor a la respuesta
            nueva_respuesta = respuesta_form.save(commit=False)
            nueva_respuesta.pregunta = pregunta
            nueva_respuesta.autor = request.user  # O el usuario actual
            nueva_respuesta.save()
            # Redirige o realiza cualquier acción deseada después de responder

    else:
        respuesta_form = RespuestaForm()  # Crea un formulario vacío para respuestas

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

def responder_pregunta(request, pregunta_id):
    pregunta = Pregunta.objects.get(pk=pregunta_id)

    if request.method == 'POST':
        # Procesa el formulario de respuesta
        form = RespuestaForm(request.POST)
        if form.is_valid():
            nueva_respuesta = form.save(commit=False)
            nueva_respuesta.autor = request.user
            nueva_respuesta.pregunta = pregunta  #asocia la respuesta a la pregunta
            nueva_respuesta.save()
            return redirect('detalle_pregunta', pregunta_id=pregunta_id)
    else:
        form = RespuestaForm()

    return render(request, 'preguntas/responder_pregunta.html', {'form': form, 'pregunta': pregunta})






