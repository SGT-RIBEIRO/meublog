from django.contrib import admin
from .models import Comentario, Post

#admin.site.register(Post)
#admin.site.register(Comentario)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'autor', 'publicado', 'status')
    list_filter = ('status', 'criado', 'publicado', 'autor')
    search_fields = ('titulo', 'corpo')
    prepopulated_fields = {'slug': ('titulo',)}
    raw_id_fields = ('autor',)
    date_hierarchy = 'publicado'
    ordering = ('status', '-publicado')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'ativo')
    list_filter = ('ativo', 'nome')
    search_fields = ('nome', 'email')
    raw_id_fields = ('fk_post',)
    #prepopulated_fields = {'nome': ('nome',)}
    date_hierarchy = 'atualizado'