from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comentario, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['titulo', 'resumen', 'contenido', 'imagen', 'categorias', 'fecha_publicacion'] 

class crearusuario(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido')
    last_name = forms.CharField(max_length=30, required=True, help_text='Requerido')
    email = forms.EmailField(required=True, help_text='Requerido')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(crearusuario, self).save(commit=False)
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(required=False, help_text='Opcional')  # Campo para la foto

    class Meta:
        model = Profile
        fields = ('photo',)



class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['cuerpo_comentario']

# forms.py

