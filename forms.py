from django import forms
from django.core.mail import EmailMessage
from django.forms.fields import EmailField
from .models import Comentario, Post

#Compartilhar post
class EmailPost(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    destino = forms.EmailField()
    coments = forms.CharField(required=False, widget=forms.Textarea)

    def enviar_email(self, meupost):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        destino = self.cleaned_data['destino']
        coments = self.cleaned_data['coments']

        conteudo = f"Recomendo ler o post: {meupost.titulo} Comentarios: {coments}"

        mail = EmailMessage(
            subject=f"Recomendo este Post",
            body=conteudo,
            from_email='contato@meublog.com.br',
            to=[destino,],
            headers={'Reply-To': email}
        )

        mail.send()

#Comentario
class ComentarioForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    corpo = forms.CharField(required=True, widget=forms.Textarea)

    def enviar_comentario(self, post):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        corpo = self.cleaned_data['corpo']

        comentario = Comentario()
        comentario.nome = nome
        comentario.email = email
        comentario.corpo = corpo
        comentario.fk_post = Post.publicados.get(id=post.id)
        comentario.save()

        
