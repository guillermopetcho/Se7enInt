# Informatorio Proyecto Final ‐ Implementaciones

![Screencast from 10-18-2024 08_52_00 PM](https://github.com/user-attachments/assets/0636d38b-7fae-411a-b142-8ea9457c307d)



## Lista de implementaciones: 

Primero es necesario seguir los pasos de configuracion de DJANGO
Segundo es necesario tener los requeriments.txt instalado como se aclaro anteriormente
Tercero se agradece seguirme, comentar o darle fav al proyecto.

code : [Se7enInt](https://github.com/guillermopetcho/Se7enInt)

Documentacion utilizada para implementar:

* [Global-Mentoring--Certified-python](https://github.com/guillermopetcho/Global-Mentoring--Certified-python)
* Chatgpt
* [Informatorio - Repositorio](https://github.com/guillermopetcho/Campus-Informatorio-Chaco/tree/Etapa-2)
* [Proyecto python Informatorio](https://github.com/guillermopetcho/grupo7)

Instructores:

[@PabloAlonso](https://github.com/codewithpablo)

[@natalibogarin](https://github.com/natalibogarin)


# Implementaciones 

### Necesariamente se tiene que contar con el proyecto base configurado:
[Configuracion necesaria antes de comenzar](https://github.com/guillermopetcho/Campus-Informatorio-Chaco/wiki/Implementaciones-DJANGO)


***

### Inicio o Portada: 
Donde se mostraran una selección de las publicaciones mas recientes o destacadas. Proporciona una visión general del contenido del blog y per-
mite a los visitantes explorar fácilmente las ultimas actualizaciones.

### Acerca de: 
En esta sección se proporciona información sobre le blog y su propósito. Puede incluir una breve descripción del equipo detrás del blog.

[Función de navegacion (Inicio, Contacto, Acerca de)](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-Funciones-de-flujo-de-usuario)

[Función de Crear - Editar el Post](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-'Crear'-y-'Editar'-posts)

[Función de Mostrar Post](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-Mostrar-posts)


### Contacto: 
Ofrece a los visitantes una forma de ponerse en contacto con el equipo que administra el blog, ya sea a través de un
formulario de contacto, dirección de correo electrónico o incluso a enlaces a las redes sociales del grupo.

[Función de 'Contacto' con Administradores](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-Funcion-de-contacto-con-administrador)

## Funcionalidades del Blog

### Categorías y Filtrado de Posts: 
Donde se dividirá el contenido del blog en categorías temáticas claras y organizadas.

### Filtrar publicaciones por: 
* Categoría.
* Antigüedad (asc y desc).
* Orden alfabético (asc y desc).


[Filtrado - Categoria, Antigüedad, Orden alfabético](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-Funciones-de-filtrado-de-posts)

***

## Escala de privilegios


### El perfil Visitante

* Navegar por la web.
* Filtrar los diferentes posteos.
* Leer artículos.
* Registrarse y loguearse en la web.

[Implementacion - Registrar Usuario](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-Registrar-usuarios)

[Implementacion - Login Usuario](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-Login)

### El perfil Miembro o Usuario registrado:

[Implementacion - Logout](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-Logout)

[Implementacion - Comentarios (crear, edita y eliminar)](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-Funcion-'Crear'-y-'Editar'-comentarios)



Al registrarse, el usuario cuenta con los siguientes privilegios:

* Navegar por al web.
* Comentar los distintos artículos.
* Editar o eliminar sus propios comentarios.
* Desloguearse.


### El perfil Colaborador:

* Cargar, Editar y Eliminar artículos, fotos asociadas a los mismos y comentarios de los demás usuarios.
* Categorizar los distintos artículos.

Función de Crear y Editar permite categorizar el posts

[Función de Crear - Editar los posts](https://github.com/guillermopetcho/Se7enInt/wiki/views-%E2%80%90-'Crear'-y-'Editar'-posts)



![Screenshot from 2024-10-11 15-43-41](https://github.com/user-attachments/assets/11785e65-f0c7-43f0-a1d7-21fe8e3d64f4)





***
Aparte se agrego implementaciones:

* Pagina de Perfil de usuario


## Implementaciones en archivos de la pagina 'blog'

[Definición correcta de rutas - urls.py](https://github.com/guillermopetcho/Se7enInt/wiki/URLSPATTERNS)

## Implementaciones en archivos de la app 'myblog'

[Librerías y módulos utilizados en views](https://github.com/guillermopetcho/Se7enInt/wiki/Librer%C3%ADas-y-m%C3%B3dulos-utilizados-en-views)


[Models ‐ Categoria,Post,Comentario,MensajeContacto,Profile](https://github.com/guillermopetcho/Se7enInt/wiki/Models-%E2%80%90-Categoria,Post,Comentario,MensajeContacto,Profile)

[Forms - Post,-Usuario,-Perfil,-Comentario](https://github.com/guillermopetcho/Se7enInt/wiki/Forms-%E2%80%90-Post,-Usuario,-Perfil,-Comentario)


[Panel de control de Admin](https://github.com/guillermopetcho/Se7enInt/wiki/Admin.py)

## Templates

[Template - Base](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Base.html)

[Template - Inicio](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Inicio)

[Template - Acerca_de](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Acerca_de.html)

[Template - Contacto](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Contacto)

[Template - Detalles-del-Post](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Detalles-del-Post)

[Template - Signup,-Login,-Logout](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Signup,-Login,-Logout)

[Template - Crear-y-Editar-Post](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Crear-y-Editar-Post)

[Template - Perfil_usuario](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Perfil_usuario)

[Template - Filtrado_Categorias](https://github.com/guillermopetcho/Se7enInt/wiki/Templates-%E2%80%90-Filtrado_categorias)
