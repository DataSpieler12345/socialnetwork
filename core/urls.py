# Ruta: socialnetwork/core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 🔐 Autenticación
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 🏠 Home y Feed
    path('', views.home_view, name='home'),
    path('feed/', views.post_list_create_view, name='feed'),

    # 📄 Detalle de publicación y comentarios
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/add_comment/', views.add_comment_to_post, name='add_comment_to_post'),

    # ❤️ Me gusta
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),

    # 👤 Perfil de usuario
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.follow_unfollow_view, name='follow_unfollow'),

    # 🔄 Listas de seguidores y seguidos
    path('profile/<str:username>/following/', views.following_list_view, name='following_list'),
    path('profile/<str:username>/followers/', views.followers_list_view, name='followers_list'),
]
