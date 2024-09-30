from django.contrib import admin
from .models import CardIssuer, CreditCard, CardCategory, Post,FAQ

class CreditCardInline(admin.TabularInline):
    model = CreditCard
    extra = 1

@admin.register(CardIssuer)
class CardIssuerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)
    filter_horizontal = ('credit_cards',)  # Correctly specify ManyToManyField

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_type', 'issuer', 'annual_fee', 'joining_fee', 'rating', 'active')
    search_fields = ('name', 'card_type', 'issuer__name')
    list_filter = ('card_type', 'issuer', 'active')
    ordering = ('-rating',)

@admin.register(CardCategory)
class CardCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_description', 'cards_description')
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'seo_title', 'seo_description')
    search_fields = ('title', 'seo_title', 'seo_keywords')
    list_filter = ('credit_cards',)
    filter_horizontal = ('credit_cards',)  # Allows selecting multiple credit cards more easily

admin.site.register(Post, PostAdmin)



@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'issuer', 'category')
    list_filter = ('issuer', 'category')
    search_fields = ('question', 'answer')