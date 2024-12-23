from django.db import models



class Evento(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('inicio_semestre', 'Inicio de Semestre'),
        ('fin_semestre', 'Fin de Semestre'),
        ('inicio_inscripcion', 'Inicio de Inscripción de Asignaturas'),
        ('fin_inscripcion', 'Fin de Inscripción de Asignaturas'),
        ('receso_academico', 'Receso Académico'),
        ('feriado_nacional', 'Feriado Nacional'),
        ('feriado_regional', 'Feriado Regional'),
        ('inicio_solicitudes', 'Inicio de Plazos de Solicitudes Administrativas'),
        ('fin_solicitudes', 'Fin de Plazos de Solicitudes Administrativas'),
        ('inicio_beneficios', 'Inicio de Plazos para la Gestión de Beneficios'),
        ('fin_beneficios', 'Fin de Plazos para la Gestión de Beneficios'),
        ('ceremonia_titulacion', 'Ceremonia de Titulación o Graduación'),
        ('reunion_consejo', 'Reunión de Consejo Académico'),
        ('talleres_charlas', 'Talleres y Charlas'),
        ('dia_orientacion', 'Día de Orientación para Nuevos Estudiantes'),
        ('eventos_extracurriculares', 'Eventos Extracurriculares'),
        ('inicio_clases', 'Inicio de Clases'),
        ('ultimo_dia_clases', 'Último Día de Clases'),
        ('dia_puertas_abiertas', 'Día de Puertas Abiertas'),
        ('suspension_completa', 'Suspensión de Actividades Completa'),
        ('suspension_parcial', 'Suspensión de Actividades Parcial'),
    ]

    Titulo = models.CharField(max_length=200)
    Descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    TipoEvento = models.CharField(max_length=50, choices=TIPO_EVENTO_CHOICES)
    
    def __str__(self):
        return f'{self.Titulo} ({self.TipoEvento})'



class Alerta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50)  # Ejemplo: "ConflictoEvento"
    estado = models.CharField(
        max_length=20,
        choices=[("Pendiente", "Pendiente"), ("Resuelto", "Resuelto")],
        default="Pendiente"
    )
    creado_en = models.DateTimeField(auto_now_add=True)






#
#class EventoAcademico(models.Model):
#    TiposEventos = [
#        ('exam', 'Examen'),
#        ('holiday', 'Feriado'),
#        ('admin', 'Administrativo'),
#    ]
#    Titulo = models.CharField(max_length=200)
#    Descripcion = models.TextField()
#    InicioPeriodo = models.DateField()
#    FinPeriodo = models.DateField()
#    TipoEvento = models.CharField(max_length=50, choices=TiposEventos)
#
#    def __str__(self):
#        return self.title