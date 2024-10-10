from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.utils import timezone
from django.http.response import Http404 # type: ignore
from .models import Post, Comentario, Categoria
from .forms import crearusuario, ComentarioForm
from django.shortcuts import render, redirect ,get_object_or_404
from .forms import PostForm
# Create your views here.


### definicion de vistas ###


def inicio(request):
    ultimosposts = Post.objects.all().order_by('fecha_publicacion')[:4]  # Cambia si necesitas limitar e numero de posts
    return render(request, 'inicio.html', {'ultimosposts': ultimosposts})

def contactos(request):
    return render(request, 'contacto.html')

def acerca_de(request):
    administradores = User.objects.filter(is_staff=True)  # Filtrar solo los usuarios administradores
    return render(request, 'acerca_de.html', {'administradores': administradores})

def perfil_usuario(request, user_id):  
    usuario = get_object_or_404(User, id=user_id)
    return render(request, 'perfil_usuario.html', {'usuario': usuario})

### decorador para verificar si el usuario es colaborador o administrador ###
def es_colaborador_o_admin(user):
    return user.groups.filter(name='Colaboradores').exists() or user.is_staff

### definicion de funciones ###
"""def lista_posts(request):
    posts = Post.objects.all().order_by('fecha_publicacion')
    return render(request, 'posts.html', {'posts': posts})
"""


def listar_posts(request):
    posts = Post.objects.all()  # Obtén todos los posts
    return render(request, 'base.html', {'posts': posts})


def listar_categorias(request):
    categorias = Categoria.objects.all()  # Obtén todas las categorías
    posts = Post.objects.all()  # Puedes agregar esto si deseas también listar los posts
    return render(request, 'base.html', {'categorias': categorias, 'posts': posts})

def listar_posts_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categorias=categoria)  # Filtra los posts por la categoría seleccionada

    return render(request, 'base.html', {
        'posts': posts,
        'categoria': categoria,
        'categorias': Categoria.objects.all(),  # Pasamos también las categorías para el aside
    })

def filtrar_por_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    posts_filtrados = categoria.posts.all()  # Obtén los posts asociados a la categoría
    return render(request, 'filtrado_categoria.html', {'categoria': categoria, 'posts': posts_filtrados})


def post_detalle(request, post_id):
    global es_colaborador, es_administrador
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all()
    es_colaborador = request.user.groups.filter(name='Colaborador').exists()
    es_administrador = request.user.is_staff
    
        # verifica si el usuario esta autenticado
    usuario_logeado = request.user.is_authenticated

    # identificar si se esta editando un comentario
    comentario_id = request.GET.get('edit_comentario', None)
    comentario_a_editar = None
    ###########################################################

    if comentario_id:
        comentario_a_editar = get_object_or_404(Comentario, id=comentario_id)

    if request.method == 'POST':
        if 'editar_comentario' in request.POST:
            form = ComentarioForm(request.POST, instance=comentario_a_editar)
            if form.is_valid():
                form.save()
                return redirect('post_detalle', post_id=post.id)
        else:
            # Manejar otros formularios (por ejemplo, añadir un nuevo comentario)
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
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.autor = request.user  # Asigna al usuario autenticado como el autor
                post.save()
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
    if request.user == comentario.autor_comentario or request.user.is_staff or request.es_colaborador:  # Solo el autor o admin pueden eliminar
        comentario.delete()
    return redirect('post_detalle', id=comentario.post.id)

@login_required
def editar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('post_detalle', id=comentario.post.id)
    else:
        form = ComentarioForm(instance=comentario)
    
    return render(request, 'editar_comentario.html', {'form': form, 'comentario': comentario})


"""
## version 6
def post_detalle(request, post_id):
    global es_colaborador, es_administrador
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all()
    es_colaborador = request.user.groups.filter(name='Colaborador').exists()
    es_administrador = request.user.is_staff
    

    # Verifica si el usuario está autenticado
    usuario_logeado = request.user.is_authenticated

    if request.method == 'POST': # hacer un POST 
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor_comentario = request.user  # O el valor correspondiente
            comentario.save()
            return redirect('post_detalle', post_id=post.id)
    else:
        form = ComentarioForm()
    
    return render(request, 'post_detalle.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'usuario_logeado': usuario_logeado,
        'colaborador': es_colaborador,
        'administrador': es_administrador,
    })
"""

"""def editar_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detalle', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'editar_post.html', {
        'form': form,
        'post': post,  # Pasamos el post al contexto
    })

"""




### version 5
"""def inicio(request):
    ultimosposts = Post.objects.all().order_by('-fecha_publicacion')[:3]
    return render(request, 'inicio.html', {'ultimosposts': ultimosposts})"""


"""def inicio(request):
    ultimosposts = Post.objects.all().order_by('-fecha_publicacion')[:3]
    return render(request, 'inicio.html', {'ultimosposts': ultimosposts})
"""
"""def postdetalle(request, id):
    #try:
    data = Post.objects.get(id=id) # Obtiene el post
    #comentarios = Comentario.objects.filter(post=data, aprobado=True) # Filtra los comentarios para que aparezcan solo los que han sido aprobados
    comentarios = Comentario.objects.filter(post=data)
    #except Post.DoesNotExist:
    #    raise Http404('No existe el post') # Maneja el error de post no encontrado
    
    #context = {'post': data, 'comentarios': comentarios}
    context = {'post': data,'comentarios': comentarios} # Crea un diccionario con los datos
    return render(request, 'post_detalle.html', context) # Renderiza la plantilla

"""


"""def postdetalle(request, id):
    # Utiliza get_object_or_404 para simplificar el manejo de errores
    post = get_object_or_404(Post, id=id)  # Obtiene el post o devuelve un 404 si no existe
    comentarios = Comentario.objects.filter(post=post)  # Filtra los comentarios aprobados

    # Crea un diccionario con los datos
    context = {
        'post': post,
        'comentarios': comentarios,
    }
    
    return render(request, 'post_detalle.html', context)  # Renderiza la plantilla
"""
####


"""def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')  # Redirige al inicio después de registrarse
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

"""
## 02/10  
"""
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/form_evento.html', {'form': form})

def listar_eventos(request):
    eventos = Eventos.objects.all()

    query = request.GET.get('titulo', '')

    if query:
        eventos = eventos.filter(titulo__icontains=query)

    paginator = Paginator(eventos, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'eventos/listar_eventos.html', {'page_obj':page_obj,'query': query })

def detalle_evento(request, id):
    try:
        evento = Eventos.objects.get(id=id)
    except Eventos.DoesNotExist:
        return HttpResponse("No existe el evento",status=404)

    return render(request, "eventos/detalles_evento.html",{"evento":evento})
"""



"""def index(request):
    ultimosposts = Post.objects.all().order_by('fecha_publicacion').reverse()[:3]
    return render(request, 'inicio.html', {'ultimosposts':ultimosposts})

def lista_posts(request):
    posts = Post.objects.all().order_by('fecha_publicacion')
    return render(request, 'posts.html',{'posts':posts})

def postdetalle(request, id):
    try:
        data = Post.objects.get(id=id)
        comentarios = Comentario.objects.filter(aprobado=True)
    except Post.DoesNotExist:
        raise Http404 ('No existe el post')
    
    context = {'post':data, 'comentarios':comentarios}
    return render(request, 'post_detalle.html', context)

"""
"""def home_view(request):
    return HttpResponse('Hello World')


class IndexView(View):
    def get(self, request):
        return HttpResponse('Pagina principal')
    
class AboutView(View):
    template_name = 'inicio.html'"""