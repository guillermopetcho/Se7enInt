from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.contrib import messages, admin
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponseForbidden  # Para manejar permisos denegados
from django.http.response import Http404 # type: ignore
from .models import Post, Comentario, Categoria,MensajeContacto, Profile
from .forms import crearusuario, ProfileForm,PostForm,ComentarioForm
from django.db.models import Count


# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout


def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciado sesión con éxito.')
                return redirect('inicio')  # Redirige a la página de inicio después de iniciar sesión
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    messages.success(request, 'Has cerrado sesión con éxito.')  # Mensaje de éxito
    return redirect('inicio')  # Redirige a la página de inicio o a donde desees




### definicion de vistas ###
def inicio(request):
    ultimos_posts = Post.objects.all().order_by('fecha_publicacion')[:4]
    primeros_posts = Post.objects.all().order_by('-fecha_publicacion')[:4]
    colaborador = request.user.groups.filter(name='Colaborador').exists()
    return render(request, 'inicio.html', {
        'ultimos_posts': ultimos_posts,
        'primeros_posts': primeros_posts,
        'colaborador': colaborador,
        'mostrar_categorias': True,
        'mostrar_fechas': True
    })

def contactos(request):
    return render(request, 'contacto.html', {'mostrar_categorias': False, 'mostrar_fechas': False})

def acerca_de(request):
    administradores = User.objects.filter(is_staff=True)  # Filtrar solo los usuarios administradores
    return render(request, 'acerca_de.html', {'administradores': administradores,'mostrar_categorias': False,'mostrar_fechas': False})

@login_required
def perfil_usuario(request, user_id):  
    # Obtener el usuario cuyo perfil se está viendo
    usuario = get_object_or_404(User, id=user_id)
    # Obtener el perfil relacionado con ese usuario
    profile = get_object_or_404(Profile, user__id=user_id)
    
    # Verificar si el usuario autenticado pertenece al grupo "Colaborador"
    colaborador = request.user.groups.filter(name='Colaborador').exists()

    # Verificar si el usuario autenticado está viendo su propio perfil
    es_perfil_propio = request.user == usuario

    # Pasar al template el usuario del perfil, y si es colaborador o es su propio perfil
    return render(request, 'perfil_usuario.html', {
        'usuario': usuario,  # El usuario cuyo perfil se está visualizando
        'profile': profile,  # El perfil del usuario que se está visualizando
        'colaborador': colaborador,  # Si el usuario autenticado es colaborador
        'es_perfil_propio': es_perfil_propio,  # Si el perfil es del usuario autenticado
        'mostrar_categorias': False,
        'mostrar_fechas': False,
    })


# Verifica si el usuario es colaborador o administrador (staff)
# Función para verificar si el usuario es colaborador o admin
def es_colaborador_o_admin(user):
    if not user.is_authenticated:
        return False
    
    # Verificar si el grupo "Colaborador" existe en la base de datos
    if not Group.objects.filter(name='Colaborador').exists():
        print("El grupo 'Colaborador' no existe.")
        return False

    # Verificar si el usuario pertenece al grupo 'Colaborador' o si es staff
    return user.groups.filter(name='Colaborador').exists() or user.is_staff

# Verifica si el usuario pertenece al grupo 'Colaborador'
def colaborador(request):
    es_colaborador = request.user.groups.filter(name='Colaborador').exists()

    context = {
        'colaborador': es_colaborador,
    }
    return render(request, 'inicio.html', context)

### decorador para verificar si el usuario es colaborador o administrador ###


def mi_vista(request):
    es_colaborador = request.user.is_authenticated and request.user.groups.filter(name='colaborador').exists()
    return render(request, 'inicio.html', {'colaborador': es_colaborador})





def listar_posts(request):
    posts = Post.objects.all()  # Obtén todos los posts
    categorias = Categoria.objects.all()  # Obtén todas las categorías
    ultimosposts = Post.objects.all().order_by('fecha_publicacion')  # Cambia si necesitas limitar e numero de post
    ultimos_mensajes = MensajeContacto.objects.order_by('-fecha_envio')[:3]
    ## implementacion

    # Filtrar posts si hay un parámetro de categoría en la URL
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = posts.filter(categorias__id=categoria_id)

    return render(request, 'inicio.html', 
                  {'ultimosposts': ultimosposts, 
                   'categorias': categorias ,
                   'mostrar_categorias': True,
                   'mostrar_fechas': True,
                   'ultimos_mensajes': ultimos_mensajes
                   })


def listar_categorias(request):
    categorias = Categoria.objects.all()  # Obtén todas las categorías
    posts = Post.objects.all()  # Puedes agregar esto si deseas también listar los posts
    return render(request, 'base.html', {'categorias': categorias,
                                           'posts': posts,
                                           'mostrar_cargas': True,
                                           'mostrar_fechas': True})


def listar_posts_por_categoria(request, categoria_id):
    global categoria,categorias
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categorias=categoria)  # Filtra los posts por la categoría seleccionada
    categorias = Categoria.objects.all()  # Obtén todas las categorías para el aside


    return render(request, 'filtrado_categorias.html', {
        'posts': posts,
        'categorias': categorias,  # Pasa las categorías para el aside
        'mostrar_categorias': True,
        'mostrar_fechas': True,
        'mostrar_cargas': True
    })

def listar_posts_alfabeticamente(request):

    categorias = Categoria.objects.all()  # Asegúrate de obtener las categorías


    orden = request.GET.get('orden', 'asc')  # Obtener el parámetro de orden de la URL
    if orden == 'desc':
        ultimosposts = Post.objects.all().order_by('-titulo')[:4]  # Ordenar de Z a A
    else:
        ultimosposts = Post.objects.all().order_by('titulo')[:4]  # Ordenar de A a Z

    return render(request, 'inicio.html', {'ultimosposts': ultimosposts, 
                                           'mostrar_cargas': True,
                                           'categorias': categorias, 
                                           'mostrar_fechas': True,
                                           'mostrar_categorias': True})


def fechas(request, tipo):
    categorias = Categoria.objects.all()  # Asegúrate de obtener las categorías
    if tipo == 'recientes':
        ultimosposts = Post.objects.all().order_by('-fecha_publicacion')[:4]  # Más recientes
    elif tipo == 'antiguos':
        ultimosposts = Post.objects.all().order_by('fecha_publicacion')[:4]  # Más antiguos
    else:
        ultimosposts = Post.objects.all()  # O una lista vacía, según lo que desees
    return render(request, 'inicio.html', {'ultimosposts': ultimosposts,
                                           'categorias': categorias, 
                                           'mostrar_cargas': True, 
                                           'mostrar_fechas': True,
                                           'mostrar_categorias': True})


def post_detalle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all()
    es_colaborador = request.user.groups.filter(name='Colaborador').exists()
    es_administrador = request.user.is_staff
    usuario_logeado = request.user.is_authenticated

    comentario_a_editar = None

    # Verificar si se va a editar un comentario
    comentario_id = request.GET.get('edit_comentario', None)
    if comentario_id:
        comentario_a_editar = get_object_or_404(Comentario, id=comentario_id)

    if request.method == 'POST':
        # Intentar editar un comentario o crear uno nuevo
        form, comentario_a_editar = procesar_comentario(request, post, comentario_a_editar)

        if form and form.is_valid():
            return redirect('post_detalle', post_id=post.id)
    else:
        form = ComentarioForm()

    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'comentario_a_editar': comentario_a_editar,
        'usuario_logeado': usuario_logeado,
        'colaborador': es_colaborador,
        'administrador': es_administrador,
        'mostrar_cargas': False, 
        'mostrar_fechas': False,
    }
    return render(request, 'post_detalle.html', context)


def procesar_comentario(request, post, comentario_a_editar):
    if comentario_a_editar:
        # Verifica si el usuario es el autor, un administrador o un colaborador
        if (
            comentario_a_editar.autor_comentario == request.user or
            request.user.is_staff or
            request.user.groups.filter(name='Colaboradores').exists()
        ):
            # Editar un comentario existente
            form = ComentarioForm(request.POST, instance=comentario_a_editar)
            if form.is_valid():
                # Mantener el autor original del comentario
                comentario_original = comentario_a_editar.autor_comentario
                form.save()

                # Mostrar una alerta si quien edita no es el autor original
                if request.user != comentario_original:
                    messages.warning(request, f'El comentario ha sido editado por {request.user.username}.')
                else:
                    messages.success(request, 'Comentario editado con éxito.')

                return form, comentario_a_editar
    else:
        # Crear un nuevo comentario
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.post = post
            nuevo_comentario.autor_comentario = request.user
            nuevo_comentario.save()
            messages.success(request, 'Comentario creado con éxito.')
            return form, None

    return None, None  # Si no se procesó nada



def signup(request):
    if request.method == 'POST':
        user_form = crearusuario(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)  # Asegúrate de manejar archivos (imágenes)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Verifica si ya existe un perfil para el usuario
            profile, created = Profile.objects.get_or_create(user=user)
            
            if created:  # Solo guarda si el perfil fue creado y no existía antes
                profile.photo = profile_form.cleaned_data['photo']  # Asigna la imagen si fue subida
                profile.save()  # Guarda el perfil con la foto
            
            messages.success(request, 'Usuario creado con éxito.')
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('inicio')
    else:
        user_form = crearusuario()
        profile_form = ProfileForm()

    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

### con logeo ###


@login_required
def crear_post(request):
    # Verifica si el usuario es colaborador o administrador
    es_colaborador = request.user.groups.filter(name='Colaborador').exists()
    es_administrador = request.user.is_staff

    if es_colaborador or es_administrador:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES aquí
            if form.is_valid():
                post = form.save(commit=False) # Guarda los datos del formulario en el objeto post
                post.autor = request.user  # Asigna al usuario autenticado como el autor
                post.save()
                form.save_m2m()
                return redirect('inicio')  # Redirige a la lista de posts después de guardar
        else:
            form = PostForm()

        return render(request, 'cargar_publicacion.html', {'form': form})
    
    return render(request, 'inicio.html')

@login_required
def editar_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Asegúrate de incluir request.FILES
        if form.is_valid():
            form.save()
            return redirect('post_detalle', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'editar_post.html', {'form': form, 'post': post})


@login_required
def eliminar_post(request, post_id):
    # Obtener el post que se desea eliminar
    post = get_object_or_404(Post, id=post_id)
    
    # Verifica si el usuario es el autor o un administrador
    if post.autor == request.user or request.user.is_staff:
        if request.method == 'POST':
            post.delete()  # Elimina el post
            return redirect('inicio')  # Redirige a la página principal después de eliminar
        return render(request, 'confirmar_eliminacion.html', {'post': post})
    else:
        return HttpResponseForbidden("No tienes permiso para eliminar este post.")  # Mensaje de error si no tiene permisos


@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    post_id = comentario.post.id  # Almacenar el ID del post antes de eliminar el comentario

    # Verificar si el usuario autenticado es el autor, administrador o colaborador
    es_colaborador = request.user.groups.filter(name='Colaborador').exists()

    if request.user == comentario.autor_comentario or request.user.is_staff or es_colaborador:  # Autor, admin o colaborador pueden eliminar
        comentario.delete()
        return redirect('post_detalle', post_id=post_id)  # Redirige de nuevo al detalle del post
    else:
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")  # Mensaje de error si no tiene permisos


@login_required
def agregar_comentario(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        contenido = request.POST.get('contenido')

        if contenido:  # Verificamos que el contenido no esté vacío
            Comentario.objects.create(
                autor_comentario=request.user,
                post=post,
                cuerpo_comentario=contenido
            )
            messages.success(request, '¡Comentario agregado con éxito!')  # Mensaje de éxito
        else:
            messages.error(request, 'No puedes enviar un comentario vacío.')  # Manejo de error

        return redirect('post_detalle', post_id=post_id)  # Redirige de nuevo a la página del post

    return redirect('post_detalle', post_id=post_id)  # Redirige si no es un POST válido

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        tema = request.POST['tema']
        mensaje = request.POST['mensaje']
        archivo = request.FILES.get('archivo')  # Para el archivo opcional

        # Crear una nueva instancia del modelo
        nuevo_mensaje = MensajeContacto(
            nombre=nombre,
            email=email,
            tema=tema,
            mensaje=mensaje,
            archivo=archivo
        )
        nuevo_mensaje.save()  # Guardar en la base de datos

        messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
        return redirect('inicio')  # Redirigir a la página de inicio o a una página de agradecimiento

    return render(request, 'contacto.html')  # Cambia a tu template si es necesario

#####################################################################################################
### implementaciones apartes del informatorio ###


