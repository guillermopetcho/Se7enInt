from tkinter import Image
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Categoria(models.Model):
    nombre = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.nombre

## Creamos el post que tendra el autor
class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    resumen = models.TextField(max_length=50000)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    ## ORM
    contenido = models.TextField(max_length=50000)
    imagen = models.ImageField(null=True, blank= True,upload_to= "img/posts", help_text= "Imagen del post")
    #creamos la relacion con categorias de post a muchas categorias
    categorias = models.ManyToManyField(Categoria, related_name="posts")

    def publish(self):
        self.fecha_publicacion = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo
    
    def mostrarcomentario(self):
        return self.comentarios.filter(aprobado=True)
    

class Comentario(models.Model):
    #relacion entre uno y muchos
    autor_comentario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post",related_name='comentarios', on_delete=models.CASCADE)

    cuerpo_comentario = models.CharField(max_length=1000)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    aprobado = models.BooleanField(default=True)

    def aprobar_comentario(self):
        self.aprobado = True
        self.save()

    def __str__(self):
        return f'Comentario de {self.autor_comentario} en {self.post}'
    

    from django.db import models



class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    tema = models.CharField(max_length=50)
    mensaje = models.TextField()
    archivo = models.FileField(upload_to='archivos/', blank=True, null=True)  # Para archivos opcionales
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to="img/posts", help_text="Imagen del perfil")
    encrypted_password = models.CharField(max_length=128, blank=True, null=True)  # Campo para almacenar la contraseña encriptada

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.user.password and not self.encrypted_password:
            self.encrypted_password = self.user.password  # Almacena la contraseña encriptada del usuario
        super(Profile, self).save(*args, **kwargs)