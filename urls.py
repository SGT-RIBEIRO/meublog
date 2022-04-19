from django.urls import path
from . import views

app_name = 'meublog'

urlpatterns=[
    path('', views.ListarPostsView.as_view(), name='listar_posts'),
    path('<slug:slug>/<int:pk>', views.DetalharPostView.as_view(), name='detalhe'),
    path('sharepost/<int:pk>/', views.FormContatoView.as_view(), name='share_post'),
    path('comentarpost/<int:pk>/', views.FormComentarioView.as_view(), name='comentar_post'),
    #path('', views.listar_posts, name='listar_posts'),
    #path('<int:ano>/<int:mes>/<int:dia>/<slug:slug>/', views.detalhar_post, name='detalhe'),
]