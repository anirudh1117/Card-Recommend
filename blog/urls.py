from django.urls import path
from .views import preview_post, ckeditor_popup, PostDetailView, PostListView

urlpatterns = [
    path('admin/preview/<int:post_id>/', preview_post, name='preview_post'),
    path('ckeditor/popup/', ckeditor_popup, name='ckeditor_popup'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]
