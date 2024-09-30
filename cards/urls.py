# cards/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreditCardByIssuerSlugView, PostViewSet, PopularCreditCardList, RecentCreditCardListView, CardCategoryViewSet, CreditCardViewSet, CardIssuerViewSet

router = DefaultRouter()
router.register(r'card-issuers', CardIssuerViewSet)
router.register(r'credit-cards', CreditCardViewSet)
router.register(r'card-categories', CardCategoryViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recent-credit-cards/', RecentCreditCardListView.as_view(), name='recent-credit-cards'),
    path('popular-credit-cards/', PopularCreditCardList.as_view(), name='popular-credit-cards'),
    path('credit-cards/issuer/<slug:slug>/', CreditCardByIssuerSlugView.as_view(), name='credit-card-list-by-issuer-slug'),
]
