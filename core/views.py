from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import (
    UserRegisterForm,
    PostForm,
    CommentForm,
    ProfileForm,
)
from .models import Post, Comment, Profile


# 1️⃣ Registro de usuarios (crea perfil automáticamente)
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Crear perfil
            login(request, user)
            # Redirige al perfil recién creado
            return redirect('profile', username=user.username)
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})


# 2️⃣ Login (manejo seguro de next y redirige al perfil si no hay next)
def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url and not url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
        next_url = None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Si next_url es válido, úsalo; si no, al perfil
            return redirect(next_url or 'profile', username=user.username)
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form, 'next': next_url})


# 3️⃣ Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# 4️⃣ Home (página principal tras login)
@login_required
def home_view(request):
    return render(request, 'core/home.html')


# 5️⃣ Feed: crear posts y añadir comentarios inline
@login_required
def post_list_create_view(request):
    post_form = PostForm()
    comment_form = CommentForm()

    # Crear nuevo post
    if request.method == 'POST' and 'content' in request.POST and 'image' in request.FILES:
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')

    # Añadir comentario
    elif request.method == 'POST' and 'comment_post_id' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post = get_object_or_404(Post, id=request.POST['comment_post_id'])
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('feed')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/feed.html', {
        'form': post_form,
        'posts': posts,
        'comment_form': comment_form,
    })


# 6️⃣ Detalle de post + comentarios thread
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'core/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


# 7️⃣ Añadir comentario en su propia vista
@login_required
def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'core/add_comment.html', {
        'form': form,
        'post': post,
    })


# ➕ Vista para alternar “Me gusta” en un post
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


# 8️⃣ Editar perfil
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})


# 9️⃣ Seguir / Dejar de seguir
@login_required
def follow_unfollow_view(request, username):
    target = get_object_or_404(User, username__iexact=username)
    current_profile = request.user.profile
    if current_profile != target.profile:
        if target.profile in current_profile.following.all():
            current_profile.following.remove(target.profile)
        else:
            current_profile.following.add(target.profile)
    return redirect('profile', username=target.username)


# 🔟 Perfil de usuario (creación de posts y comentarios desde aquí)
@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User, username__iexact=username)
    profile = user_obj.profile
    posts = Post.objects.filter(author=user_obj).order_by('-created_at')
    is_following = (
        profile in request.user.profile.following.all()
        if profile != request.user.profile else False
    )

    # Nuevo post desde perfil
    post_form = PostForm()
    if request.method == 'POST' and 'new_post' in request.POST:
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('profile', username=username)

    # Nuevo comentario desde perfil
    comment_form = CommentForm()
    if request.method == 'POST' and 'comment_post_id' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            p = get_object_or_404(Post, id=request.POST['comment_post_id'])
            c = comment_form.save(commit=False)
            c.post = p
            c.author = request.user
            c.save()
            return redirect('profile', username=username)

    return render(request, 'core/profile.html', {
        'profile_user': user_obj,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'post_form': post_form,
        'comment_form': comment_form,
    })


# 1️⃣1️⃣ Lista de “Siguiendo”
@login_required
def following_list_view(request, username):
    user_obj = get_object_or_404(User, username__iexact=username)
    profile = user_obj.profile
    following_profiles = profile.following.all()
    return render(request, 'core/follow_list.html', {
        'title': f'Siguiendo • {user_obj.username}',
        'list_profiles': following_profiles,
        'owner': user_obj,
    })


# 1️⃣2️⃣ Lista de “Seguidores”
@login_required
def followers_list_view(request, username):
    user_obj = get_object_or_404(User, username__iexact=username)
    profile = user_obj.profile
    followers_profiles = profile.followers.all()
    return render(request, 'core/follow_list.html', {
        'title': f'Seguidores • {user_obj.username}',
        'list_profiles': followers_profiles,
        'owner': user_obj,
    })
