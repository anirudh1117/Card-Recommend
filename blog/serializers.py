# serializers.py
from rest_framework import serializers
from .models import Post, Section, Image
from cards.models import CreditCard, CardIssuer


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'name']  # Adjust fields to match your CreditCard model


class CardIssuerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardIssuer
        fields = ['id', 'issuer_name']  # Adjust fields accordingly


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'caption']


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
            'id',
            'section_type',
            'content',
            'custom_content',
            'credit_Cards',
            'card_issuers',
            'images',
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
            data['images'] = ImageSerializer(instance.images.all(), many=True).data
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
            data['credit_Cards'] = CreditCardSerializer(instance.credit_Cards.all(), many=True).data
            data['card_issuers'] = CardIssuerSerializer(instance.card_issuers.all(), many=True).data
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

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'slug',
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
        # Find the 'head' of the list (the section with no previous_section)
        head_section = obj.sections.filter(previous_section__isnull=True).first()

        # Traverse the linked-list
        ordered_sections = []
        current = head_section
        while current:
            ordered_sections.append(current)
            # Move to the next in chain
            current = getattr(current, 'next_section', None)

        return SectionSerializer(ordered_sections, many=True, context=self.context).data
