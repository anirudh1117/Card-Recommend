from django.urls import path
from .views import preview_post,ckeditor_popup

urlpatterns = [
    path('admin/preview/<int:post_id>/', preview_post, name='preview_post'),
     path('ckeditor/popup/', ckeditor_popup, name='ckeditor_popup'),
]