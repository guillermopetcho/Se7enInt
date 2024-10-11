from .models import Post
from .models import Categoria
from .models import Comentario
from django.utils.safestring import mark_safe
from django.contrib import admin

## version 2.0 

from .models import Post, Categoria, Comentario, Profile

## version 3 privilegios de usuarios

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver

## version 4.0
from .models import MensajeContacto

# Register your models here.
class CategoriasInline(admin.StackedInline):
    model = Post.categorias.through
    extra = 5



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo')  # Muestra el nombre de usuario y la foto en la lista
    search_fields = ('user__username',)  # Permite buscar por nombre de usuario




class PostAdmin(admin.ModelAdmin):
    inlines = [
        CategoriasInline
    ]
    raw_id_fields = ('autor',)  # Puedes usar autocomplete_fields si es necesario
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    search_fields = ['titulo', 'resumen', 'autor__username']
    list_filter = ('autor', 'fecha_publicacion')
    list_per_page = 25

    readonly_fields = ['noticia_img']
    
    def categoria(self, obj):
        return "\n".join([c.nombre for c in obj.categorias.all()])

    def noticia_img(self, obj):
        if obj.imagen:  # Verificamos si hay una imagen antes de renderizar
            return mark_safe(
                f'<a href="{obj.imagen.url}"><img src="{obj.imagen.url}" width="10%"/></a>'
            )
        return "No image available"
    
    fieldsets = [
        ("Contenido del post", {
            "fields": [("titulo", "resumen"), "contenido", "noticia_img", "imagen", "autor", "fecha_creacion", "fecha_publicacion"],
            "description": "Contenido del post",  
        }),
    ]

class ComentariosAdmin(admin.ModelAdmin):
    list_display = ('autor_comentario', 'cuerpo_comentario', 'post', 'fecha_creacion', 'aprobado')
    list_filter = ('aprobado', 'fecha_creacion')
    search_fields = ['autor_comentario', 'cuerpo_comentario']
    actions = ['aprobar_comentarios']

    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Ejemplo de personalización

#privelegios de usuarios

@receiver(post_migrate)
def create_user_roles(sender, **kwargs): # Crea los grupos y los permisos
    # Cargar los modelos necesarios
    Post = apps.get_model('myblog', 'Post')
    Comentario = apps.get_model('myblog', 'Comentario')
    
    # Crear los grupos
    editor_group, created = Group.objects.get_or_create(name='Colaborador')
    comentarista_group, created = Group.objects.get_or_create(name='Usuario')
    
    # Permisos de editor
    content_type_post = ContentType.objects.get_for_model(Post)
    post_permissions = Permission.objects.filter(content_type=content_type_post)
    editor_group.permissions.set(post_permissions)  # Dar todos los permisos de Post al editor
    
    # Permisos de comentarista
    content_type_comentario = ContentType.objects.get_for_model(Comentario)
    comentar_permissions = Permission.objects.filter(content_type=content_type_comentario)
    comentarista_group.permissions.set(comentar_permissions)  # Solo permisos de comentarios

    print("Roles creados y permisos asignados correctamente")


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'tema', 'fecha_envio')  # Campos a mostrar en el admin
    search_fields = ('nombre', 'email', 'tema')  # Campos por los que se puede buscar
    list_filter = ('tema', 'fecha_envio')  # Campos para filtrar la lista













# Registro de modelos
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comentario, ComentariosAdmin)
admin.site.register(Profile, ProfileAdmin)

