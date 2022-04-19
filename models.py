from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

#Posts
class PublicadosManager(models.Manager):
    def get_queryset(self):
        return super(PublicadosManager, self).get_queryset().filter(status='publicado')

class Post(models.Model):
    STATUS_CHOICES=(
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado')
    )

    object = models.Manager() #gerenciador padrão
    publicados = PublicadosManager() #gerenciador personalizados. Este é chamado na funcão view listar posts

    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100)
    corpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meublog_posts')  
    publicado = models.DateTimeField(default=timezone.now) #Na hora atual
    criado = models.DateTimeField(auto_now_add=True)# No momento em que criar 
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='rascunho')
    
    class Meta:
        ordering = ('-publicado',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return self.titulo

#Comentarios
class AtivosManager(models.Manager):
    def get_queryset(self):
        return super(AtivosManager, self).get_queryset().all()   

class Comentario(models.Model):
    STATUS_CHOICES=(
        (True, 'Ativo'),
        (False, 'Desativo')
    )

    ativosG = AtivosManager()#Gerenciador

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    corpo = models.CharField(max_length=255)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(choices=STATUS_CHOICES, default=True)
    fk_post = models.ForeignKey(Post, on_delete=models.CASCADE)#Chave Estrangeira

    def __str__(self):
        return self.corpo