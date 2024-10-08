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




from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from myblog.views import index, lista_posts, postdetalle, acerca_de, contactos
#from . import views
from myblog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="inicio"),
    path("acerca_de/", acerca_de, name="acerca_de"),  # Debería tener una vista específica para "acerca_de"
    path("contacto/", contactos, name="contacto"),    # Debería tener una vista específica para "contacto"
    path("posts/", lista_posts, name="listar_posts"),
    path("posts/<int:id>/detalle/", postdetalle, name="postdetalle"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('signup/',views.signup, name='signup'),
]


"""from django.contrib import admin
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