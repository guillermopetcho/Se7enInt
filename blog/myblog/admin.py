from .models import Post
from .models import Categoria
from .models import Comentario
from django.utils.safestring import mark_safe
from django.contrib import admin


from django.contrib import admin
from .models import Post, Categoria, Comentario
from django.utils.safestring import mark_safe

# Register your models here.
class CategoriasInline(admin.StackedInline):
    model = Post.categorias.through
    extra = 5

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

# Registro de modelos
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comentario, ComentariosAdmin)

























































"""
# Register your models here.
class CategoriasInline(admin.StackedInline):
    model = Post.categorias.through
    extra = 5

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CategoriasInline
    ]
    raw_id_fields = ('autor',)
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    search_fields = ['titulo', 'resumen', 'autor__username']
    list_filter = ('autor', 'fecha_publicacion')
    list_per_page = 25

    readonly_fields = ['noticia_img']
    
    def categoria(self, obj):
        return "\n".join([c.nombre for c in obj.categorias.all()])

    def noticia_img(self, obj):
        return mark_safe(
            '<a href= "{0}"><img src="{0}" width="10%"/></a>'.format(self.imagen_url)
        )
    
    fieldsets = [
    ("contenido del post", {
        "fields": [("titulo", "resumen"), "contenido", "noticia_img","imagen","autor", "fecha_creacion", "fecha_publicacion"],
        "description": "Contenido del post",  # Cambiado a 'description'
    }),
]


class comentariosAdmin(admin.ModelAdmin):
    list_display = ('autor_comentario', 'cuerpo_comentario','post','fecha_creacion','aprobado')
    list_filter = ('aprobado', 'fecha_creacion')
    search_fields = ['autor_comentario', 'cuerpo_comentario']
    actions = ['aprobar_comentario']

    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)

admin.site.register(Categoria,admin.ModelAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comentario,comentariosAdmin)
"""