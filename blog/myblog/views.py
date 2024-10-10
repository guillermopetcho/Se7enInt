from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponseForbidden  # Para manejar permisos denegados
from django.http.response import Http404 # type: ignore
from .models import Post, Comentario, Categoria
from .forms import crearusuario, ComentarioForm
from django.shortcuts import render, redirect ,get_object_or_404
from .forms import PostForm
# Create your views here.


### definicion de vistas ###


def contactos(request):
    return render(request, 'contacto.html', {'mostrar_categorias': False, 'mostrar_fechas': False})

def acerca_de(request):
    administradores = User.objects.filter(is_staff=True)  # Filtrar solo los usuarios administradores
    return render(request, 'acerca_de.html', {'administradores': administradores,'mostrar_categorias': False,'mostrar_fechas': False})

def perfil_usuario(request, user_id):  
    usuario = get_object_or_404(User, id=user_id)
    return render(request, 'perfil_usuario.html', {'usuario': usuario ,'mostrar_categorias': False,'mostrar_fechas': False})

### decorador para verificar si el usuario es colaborador o administrador ###
def es_colaborador_o_admin(user):
    return user.groups.filter(name='Colaboradores').exists() or user.is_staff

### definicion de funciones ###

def listar_posts(request):
    posts = Post.objects.all()  # Obtén todos los posts
    categorias = Categoria.objects.all()  # Obtén todas las categorías
    ultimosposts = Post.objects.all().order_by('fecha_publicacion')  # Cambia si necesitas limitar e numero de posts


    # Filtrar posts si hay un parámetro de categoría en la URL
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = posts.filter(categorias__id=categoria_id)

    return render(request, 'inicio.html', 
                  {'ultimosposts': ultimosposts, 
                   'categorias': categorias ,
                   'mostrar_categorias': True,
                   'mostrar_fechas': True})


def listar_categorias(request):
    categorias = Categoria.objects.all()  # Obtén todas las categorías
    posts = Post.objects.all()  # Puedes agregar esto si deseas también listar los posts
    return render(request, 'inicio.html', {'categorias': categorias, 'posts': posts})

def listar_posts_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categorias=categoria)  # Filtra los posts por la categoría seleccionada
    categorias = Categoria.objects.all()  # Obtén todas las categorías para el aside

    return render(request, 'filtrado_categorias.html', {
        'posts': posts,
        'categoria': categoria,
        'categorias': categorias,  # Pasa las categorías para el aside
        'mostrar_categorias': True,
        'mostrar_fechas': True
    })


def listar_posts_alfabeticamente(request):
    orden = request.GET.get('orden', 'asc')  # Obtener el parámetro de orden de la URL
    if orden == 'desc':
        ultimosposts = Post.objects.all().order_by('-titulo')[:4]  # Ordenar de Z a A
    else:
        ultimosposts = Post.objects.all().order_by('titulo')[:4]  # Ordenar de A a Z

    return render(request, 'inicio.html', {'ultimosposts': ultimosposts})

def listar_posts_fechas(request):
    ultimosposts = Post.objects.all().order_by('-fecha_publicacion')[:4]
    return render(request, 'inicio.html', {'ultimosposts': ultimosposts})

def post_detalle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all()
    es_colaborador = request.user.groups.filter(name='Colaborador').exists()
    es_administrador = request.user.is_staff
    
    # verifica si el usuario esta autenticado
    usuario_logeado = request.user.is_authenticated

    # identificar si se esta editando un comentario
    comentario_id = request.GET.get('edit_comentario', None)
    comentario_a_editar = None

    if comentario_id:
        comentario_a_editar = get_object_or_404(Comentario, id=comentario_id)

    if request.method == 'POST':
        # Si se está editando un comentario
        if comentario_a_editar and comentario_a_editar.autor_comentario == request.user:
            form = ComentarioForm(request.POST, instance=comentario_a_editar)
            if form.is_valid():
                form.save()
                return redirect('post_detalle', post_id=post.id)
        # Si es un nuevo comentario
        else:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                nuevo_comentario = form.save(commit=False)
                nuevo_comentario.post = post
                nuevo_comentario.autor_comentario = request.user
                nuevo_comentario.save()
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
    }
    return render(request, 'post_detalle.html', context)




def signup(request):
    if request.method == 'POST':
        form = crearusuario(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')  # Redirige al inicio despuess de registrarse
    else:
        form = crearusuario()
    
    return render(request, 'registration/signup.html', {'form': form})

### con logeo ###
@login_required
def agregar_comentario(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        contenido = request.POST.get('contenido')
        post = get_object_or_404(Post, id=post_id)
        Comentario.objects.create(autor_comentario=request.user, post=post, cuerpo_comentario=contenido)
        return redirect('post_detalle', post_id=post_id)  # Redirige de nuevo a la pag del post

    return redirect('post_detalle', post_id=post_id)  # Redirige de nuevo si no es un POST valido


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
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    post_id = comentario.post.id  # Almacenar el ID del post antes de eliminar el comentario

    if request.user == comentario.autor_comentario or request.user.is_staff:  # Solo el autor o admin pueden eliminar
        comentario.delete()
    return redirect('post_detalle', post_id=post_id)  # Redirige de nuevo al detalle del post


