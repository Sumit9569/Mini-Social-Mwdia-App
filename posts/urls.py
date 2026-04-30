from django.urls import path
from . import views

urlpatterns = [
    
    path('post/create/', views.create_post, name='create_post'),
    path('song/search/', views.search_song, name='search_song'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/archive/', views.archive_post, name='archive_post'),
]