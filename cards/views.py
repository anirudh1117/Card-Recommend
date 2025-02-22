from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from .models import CardIssuer, CreditCard, CardCategory, Post
from .serializers import CardIssuerSerializer, CreditCardSerializer, CardCategorySerializer, PostSerializer
from rest_framework.generics import ListAPIView
from rest_framework import generics



class NoPagination:
    def paginate_queryset(self, queryset, request, view=None):
        return list(queryset)  # Return all items in the queryset

    def get_paginated_response(self, data):
        return Response(data)

class CardIssuerViewSet(viewsets.ModelViewSet):
    queryset = CardIssuer.objects.all()
    serializer_class = CardIssuerSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ['name']
    ordering = ['name']  # Default ordering

    # Use the NoPagination class to disable pagination
    #pagination_class = NoPagination

class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all().order_by('name')  # Sort by name
    serializer_class = CreditCardSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ['name']  # Allow ordering by name
    ordering = ['name']  # Default ordering by name

class CardCategoryViewSet(viewsets.ModelViewSet):
    queryset = CardCategory.objects.all()
    serializer_class = CardCategorySerializer



class RecentCreditCardListView(generics.ListAPIView):
    queryset = CreditCard.objects.all().order_by('-card_upload_date')[:3]  # Order by most recent and limit to 3
    serializer_class = CreditCardSerializer



class PopularCreditCardList(generics.ListAPIView):
    queryset = CreditCard.objects.filter(popular=True, active=True)[:3]
    serializer_class = CreditCardSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer




class CreditCardByIssuerSlugView(generics.ListAPIView):
    serializer_class = CreditCardSerializer
    pagination_class = None  # Disable pagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        try:
            issuer = CardIssuer.objects.get(slug=slug)
            return CreditCard.objects.filter(issuer=issuer)
        except CardIssuer.DoesNotExist:
            return CreditCard.objects.none()