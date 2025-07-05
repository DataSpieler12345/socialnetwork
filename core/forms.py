# socialnetwork/core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment, Profile

# Formulario de registro de usuarios
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Formulario para crear publicaciones
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']


# Formulario para crear comentarios
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '',  # Eliminamos la etiqueta "Content:"
        }
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': 2,
                    'placeholder': 'Escribe un comentario…',
                    'required': False,          # Quita la validación HTML "required"
                    'class': 'form-control',    # Clase Bootstrap para estilizar
                }
            ),
        }


# Formulario para editar perfil
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'bio',
            'location',
            'birth_date',
            'status',
        ]
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
