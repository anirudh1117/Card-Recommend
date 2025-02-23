from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer,PostListSerializer

from django.shortcuts import render, get_object_or_404
from .models import Post, Section
from .admin import SectionAdminForm

def preview_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sections = Section.objects.filter(post=post).order_by('id')  # Ensure sections are in order
    return render(request, 'blog/preview_post.html', {'post': post, 'sections': sections})


def ckeditor_popup(request):
    form = SectionAdminForm()
    return render(request, 'blog/ckeditor_popup.html', {'form': form})


class PostDetailView(RetrieveAPIView):
    """
    Retrieves a single Post by slug if is_published=True.
    Returns sections in a linked-list order.
    """
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True).prefetch_related(
            'sections__images',
            'sections__credit_Cards',
            'sections__card_issuers',
        )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PostListView(generics.ListAPIView):
    """
    GET: List all Post objects without section data.
    """
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostListSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        category_slug = self.request.query_params.get('category')
        tag_slug = self.request.query_params.get('tag')

        # Filter by Category slug if present
        if category_slug:
            qs = qs.filter(category__name_slug=category_slug)

        # Filter by Tag slug if present
        if tag_slug:
            qs = qs.filter(tags__name_slug=tag_slug)

        return qs



