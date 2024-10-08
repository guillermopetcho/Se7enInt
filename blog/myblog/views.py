#from django.http import HttpResponse
#from django.views import View
from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.http.response import Http404 # type: ignore
# Create your views here.



def listar_posts(request):
    posts = Post.objects.all().order_by('fecha_publicacion')
    return render(request, 'inicio.html',{'posts':posts})

def postdetalle(requist, id):
    try:
        data = Post.objects.get(id=id)
        comentario = comentario.objects.filter(aprobado=True)
    except Post.DoesNotExist:
        raise Http404 ('No existe el post')
    
    context = {'post':data, 'comentarios':comentario}
    return render(requist, 'post_detalle.html', context)


"""def home_view(request):
    return HttpResponse('Hello World')

def index(request):
    return render(request, 'inicio.html')

class IndexView(View):
    def get(self, request):
        return HttpResponse('Pagina principal')
    
class AboutView(View):
    template_name = 'inicio.html'"""