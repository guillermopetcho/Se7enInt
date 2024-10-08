from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    ## ORM
    contenido = models.CharField(max_length=5000)
    imagen = models.ImageField(null=True, blank= True,upload_to= "img/posts", help_text= "Imagen del post")
    categorias = models.ManyToManyField('Categoria', related_name="posts")

    def publish(self):
        self.fecha_publicacion = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo
    
    def mostrarcomentario(self):
        return self.comentarios.filter(aprobado=True)
    
## ORM
## creamos categoria

class Categoria(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class comentarios(models.Model):
    #relacion entre uno y muchos
    autor_comentario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post",related_name='comentarios', on_delete=models.CASCADE)

    cuerpo_comentario = models.CharField(max_length=1000)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    aprobado = models.BooleanField(default=True)

    def aprobarcomentario(self):
        self.aprobado = True
        self.save()