from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    add_comment
)
from . import views

urlpatterns=[
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # Specific routes must come before the generic detail route to avoid shadowing
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<slug:slug>/comment/', add_comment, name='post-add-comment'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('about/', views.about, name='blog-about')
]