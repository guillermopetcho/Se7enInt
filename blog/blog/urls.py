"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#version de control v4
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from apps.myblog.views import *
from apps.myblog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path("inicio/", listar_posts, name="inicio"),  # Ruta para la vista de inicio
    path('', listar_posts, name='listar_posts'),  # Ruta principal para listar posts    #path('posts/', listar_posts, name='listar_posts'),
    
    path("acerca_de/", acerca_de, name="acerca_de"),  # Ruta para la vista "Acerca de"
    path("contacto/", contactos, name="contacto"),    # Ruta para la vista de contacto
    
    path('categoria/<int:categoria_id>/', listar_posts_por_categoria, name='listar_posts_por_categoria'),
    path('posts/alfabeticamente/<int:categoria_id>/', views.listar_posts_por_categoria, name='listar_posts_por_categoria'),
    path('categoria/<int:categoria_id>/', views.listar_posts_por_categoria, name='listar_posts_por_categoria'),


    path('post/<int:post_id>/comentario/', agregar_comentario, name='agregar_comentario'),
    path('post/<int:post_id>/', post_detalle, name='post_detalle'),
    path('post/<int:id>/', post_detalle, name='post_detalle'),
    path('post/<int:id>/editar/', editar_post, name='editar_post'),
    path('posts/', listar_posts, name='listar_posts'),
    path('posts/alfabeticamente/', views.listar_posts_alfabeticamente, name='listar_posts_alfabeticamente'),
    path('posts/fechas/<str:tipo>/', views.fechas, name='listar_posts_fechas'),  # Captura el argumento "tipo"
    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Ruta para iniciar sesión
    path('signup/', views.signup, name='signup'),# Ruta para registro
    path('logout/', cerrar_sesion, name='cerrar_sesion'),  # Ruta para cerrar sesión

    path('perfil_usuario/<int:user_id>/', perfil_usuario , name='perfil_usuario'),
    path('enviar_mensaje/', enviar_mensaje, name='enviar_mensaje'),
    
    path('crear_post/', crear_post, name='cargar_publicacion'),
    path('comentario/<int:comentario_id>/eliminar/', eliminar_comentario, name='eliminar_comentario'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),

    #path('categoria/<int:id>/', views.filtrar_por_categoria, name='filtrar_por_categoria'),
    #/posts/alfabeticamente/?orden=asc
    #path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),  # Ruta para cerrar sesión
    #path('editar_comentario/<int:id>/', views.editar_comentario, name='editar_comentario'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




