# serializers.py
from rest_framework import serializers
from .models import Post, Section, Image, MetaKeywords, Tag, Category
from cards.models import CreditCard, CardIssuer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name', 'name_slug']


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'name_slug', 'description']


class CreditCardSerializer(serializers.ModelSerializer):

    card_image = serializers.SerializerMethodField()

    def get_card_image(self, obj):
        """
        Return a fully qualified URL for card_image if it exists.
        """
        request = self.context.get('request')
        if obj.card_image:
            return request.build_absolute_uri(obj.card_image.url)
        return None

    class Meta:
        model = CreditCard
        fields = '__all__'


class CardIssuerSerializer(serializers.ModelSerializer):

    issuer_image = serializers.SerializerMethodField()
    cards_image = serializers.SerializerMethodField()

    def get_cards_image(self, obj):
        """
        Return a fully qualified URL for cover_image if it exists.
        """
        request = self.context.get('request')
        if obj.cards_image:
            return request.build_absolute_uri(obj.cards_image.url)
        return None

    def get_issuer_image(self, obj):
        """
        Return a fully qualified URL for cover_image if it exists.
        """
        request = self.context.get('request')
        if obj.issuer_image:
            return request.build_absolute_uri(obj.issuer_image.url)
        return None

    class Meta:
        model = CardIssuer
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        """
        Return a fully qualified URL for cover_image if it exists.
        """
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Image
        fields = ['image', 'caption']


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializer that conditionally includes fields based on section_type.
    """
    credit_Cards = CreditCardSerializer(many=True, read_only=True)
    card_issuers = CardIssuerSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = [
            'section_type',
            'content',
            'custom_content',
            'credit_Cards',
            'card_issuers',
            'images'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        section_type = instance.section_type

        if section_type in ['heading', 'subheading', 'paragraph', 'content']:
            # Keep only content
            data['content'] = instance.content
            data.pop('custom_content', None)
            data.pop('credit_Cards', None)
            data.pop('card_issuers', None)
            data.pop('images', None)

        elif section_type == 'image':
            # Keep only images
            data['images'] = ImageSerializer(
                instance.images.all(), many=True, context=self.context).data
            data.pop('content', None)
            data.pop('custom_content', None)
            data.pop('credit_Cards', None)
            data.pop('card_issuers', None)

        elif section_type == 'custom':
            # Keep only custom_content
            data['custom_content'] = instance.custom_content
            data.pop('content', None)
            data.pop('credit_Cards', None)
            data.pop('card_issuers', None)
            data.pop('images', None)

        elif section_type == 'data':
            # Keep only credit_Cards & card_issuers
            data['credit_Cards'] = CreditCardSerializer(
                instance.credit_Cards.all(), many=True, context=self.context).data
            data['card_issuers'] = CardIssuerSerializer(
                instance.card_issuers.all(), many=True, context=self.context).data
            data.pop('content', None)
            data.pop('custom_content', None)
            data.pop('images', None)

        return data


class PostSerializer(serializers.ModelSerializer):
    """
    Uses a method field 'sections' to traverse the linked-list structure:
      - find head (previous_section=None)
      - follow 'next_section' to build a chain
    """
    sections = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    category = CategoriesSerializer(many=True, read_only=True)
    meta_keywords = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        """
        Return a fully qualified URL for cover_image if it exists.
        """
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    def get_meta_keywords(self, obj):
        return ", ".join([keyword.name for keyword in obj.meta_keywords.all()])

    class Meta:
        model = Post
        fields = [
            'title',
            'description',
            'slug',
            'cover_image',
            'tags',
            'meta_keywords',
            'category',
            'created_at',
            'updated_at',
            'is_published',
            'sections',
        ]

    def get_sections(self, obj):
        """
        Build an ordered list of sections by starting from the head (previous_section=None)
        and traversing via 'next_section'.
        """
        head_section = obj.sections.filter(
            previous_section__isnull=True).first()

        ordered_sections = []
        current = head_section
        while current:
            ordered_sections.append(current)
            current = getattr(current, 'next_section', None)

        return SectionSerializer(ordered_sections, many=True, context=self.context).data


class PostListSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    category = CategoriesSerializer(many=True, read_only=True)
    meta_keywords = serializers.SerializerMethodField()

    def get_meta_keywords(self, obj):
        return ", ".join([keyword.name for keyword in obj.meta_keywords.all()])

    class Meta:
        model = Post
        fields = '__all__'
