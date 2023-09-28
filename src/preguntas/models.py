from django.db import models
from django.conf import settings


class Pregunta(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo
    
class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    contenido = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return f'Respuesta a "{self.pregunta.titulo}"'