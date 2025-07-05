from django.db import models
from django.contrib.auth.models import User

# Modelo de perfil extendido
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, blank=True)

    # Campo para seguir a otros usuarios
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Modelo de publicaciones
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ➕ Campo para llevar los "Me gusta"
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


# Modelo de comentarios
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post #{self.post.id}"
