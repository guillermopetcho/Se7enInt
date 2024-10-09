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
from myblog.views import *
from myblog import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path("", inicio, name="inicio"),  # Ruta para la vista de inicio
    path("acerca_de/", acerca_de, name="acerca_de"),  # Ruta para la vista "Acerca de"
    path("contacto/", contactos, name="contacto"),    # Ruta para la vista de contacto
    path("posts/", lista_posts, name="listar_posts"),  # Ruta para listar posts
    #path("posts/<int:id>/detalle/", postdetalle, name="postdetalle"),  # Ruta para detalles de un post
    path('post/<int:post_id>/', post_detalle, name='post_detalle'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Ruta para iniciar sesión
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),  # Ruta para cerrar sesión
    path('signup/', views.signup, name='signup'),# Ruta para registro
    path('perfil_usuario/<int:user_id>/', perfil_usuario , name='perfil_usuario'),
    path('post/<int:post_id>/comentario/', agregar_comentario, name='agregar_comentario'),
    path('crear_post/', crear_post, name='cargar_publicacion'),
    path('post/<int:id>/', post_detalle, name='post_detalle'),
    path('post/<int:id>/editar/', editar_post, name='editar_post'),
    path('comentario/<int:comentario_id>/eliminar/', eliminar_comentario, name='eliminar_comentario'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





"""
## version de control v2 - v3
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path
from myblog.views import inicio, lista_posts, postdetalle, acerca_de, contactos
#from . import views
from myblog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", inicio, name="inicio"),
    path("acerca_de/", acerca_de, name="acerca_de"),  # Debería tener una vista específica para "acerca_de"
    path("contacto/", contactos, name="contacto"),    # Debería tener una vista específica para "contacto"
    path("posts/", lista_posts, name="listar_posts"),
    path("posts/<int:id>/detalle/", postdetalle, name="postdetalle"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/',views.signup, name='signup'),
]
"""

"""
##version de control v1
from django.contrib import admin
from django.urls import path
from myblog.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index, name="inicio"),
    path("acerca_de",index, name="acerca_de"),
    path("contacto",index, name="contacto"),
    path("posts",lista_posts, name="listar_posts"),
    path("posts-detalle/<int:id>", postdetalle , name="postdetalle"),
    #path('', home_view, name='home_view'),
    #path('index', index, name='index'),

]
"""