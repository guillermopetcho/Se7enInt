from django.shortcuts import render
#from django.http import HttpResponse
#from django.views import View
from .models import Post
from django.utils import timezone
# Create your views here.



def listar_posts(request):
    posts = Post.objects.all().order_by('fecha_publicacion')
    return render(request, 'inicio.html',{'posts':posts})



"""def home_view(request):
    return HttpResponse('Hello World')

def index(request):
    return render(request, 'inicio.html')

class IndexView(View):
    def get(self, request):
        return HttpResponse('Pagina principal')
    
class AboutView(View):
    template_name = 'inicio.html'"""