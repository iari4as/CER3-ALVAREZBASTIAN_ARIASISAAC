from django.db import models

class EventoAcademico(models.Model):
    TiposEventos = [
        ('exam', 'Examen'),
        ('holiday', 'Feriado'),
        ('admin', 'Administrativo'),
    ]
    Titulo = models.CharField(max_length=200)
    Descripcion = models.TextField()
    InicioPeriodo = models.DateField()
    FinPeriodo = models.DateField()
    TipoEvento = models.CharField(max_length=50, choices=TiposEventos)

    def __str__(self):
        return self.title