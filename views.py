from django.core.mail import message
from django.shortcuts import render, get_object_or_404
from .models import Post, Comentario
from .forms import ComentarioForm, EmailPost
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages

#Posts
class ListarPostsView(ListView):
    queryset = Post.publicados.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'meublog/post/listarposts.html'


class DetalharPostView(DetailView):
    model = Post
    template_name = 'meublog/post/detalharpost.html'    
    
    def get_context_data(self, **kwargs):
        #Pega o contexto da página
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comentarios'] = Comentario.ativosG.filter(fk_post=kwargs.get('object').id)
        return context

#Form do comentarios
class FormComentarioView(FormView):
    template_name = 'meublog/post/comentar.html'
    success_url = reverse_lazy('meublog:listar_posts')
    form_class = ComentarioForm

    def get_post(self, id_post):
        try:
            return Post.publicados.get(pk=id_post)
        except Post.DoesNotExist:
            messages.error(self.request, 'O post não existe')
            reverse_lazy('meublog:listar_posts')
    
    def get_context_data(self, **kwargs):
        context = super(FormComentarioView, self).get_context_data(**kwargs)
        context['post'] = self.get_post(self.kwargs['pk'])
        return context
    
    def form_valid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        form.enviar_comentario(meupost)
        messages.success(self.request, f'Comentario enviado com sucesso')
        return super(FormComentarioView, self).form_valid(form, *args, **kwargs)

    
    def form_invalid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        messages.error(self.request, f'Comentario com erro ao enviar')
        return super(FormComentarioView, self).form_invalid(form, *args, **kwargs)

#Contato form
class FormContatoView(FormView):
    template_name = 'meublog/post/sharepost.html'
    form_class = EmailPost
    success_url = reverse_lazy('meublog:listar_posts')

    def get_post(self, id_post):
        try:
            return Post.publicados.get(pk=id_post)
        except Post.DoesNotExist:
            messages.error(self.request, 'O post não existe')
            reverse_lazy('meublog:listar_posts')

    def get_context_data(self, **kwargs):
        context = super(FormContatoView, self).get_context_data(**kwargs)
        context['post'] = self.get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        form.enviar_email(meupost)
        messages.success(self.request, f'Post {meupost.titulo} enviado com sucesso')
        return super(FormContatoView, self).form_valid(form, *args, **kwargs)

    
    def form_invalid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        messages.error(self.request, f'Post {meupost.titulo} erro ao enviar')
        return super(FormContatoView, self).form_invalid(form, *args, **kwargs)
'''
def listar_posts(request):
    posts = Post.publicados.all() #Este é o gerenciador criado
    return render(request, 'meublog/post/listarposts.html', {'posts': posts})

def detalhar_post(request, ano, mes, dia, slug, pk):
    post = get_object_or_404(Post, slug=slug, status='publicado', publicado__year=ano, publicado__month=mes, publicado__day=dia)
    comentarios = Comentario.ativosG.filter(ativo=True, fk_post=pk)
    return render(request, 'meublog/post/detalharpost.html', {'post': post, 'comentarios': comentarios})
'''