from rest_framework import serializers
from .models import CardIssuer, CreditCard, CardCategory,Post

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'

class CardIssuerSerializer(serializers.ModelSerializer):
    cr = CreditCardSerializer(many=True, read_only=True)  # Use the correct related name

    class Meta:
        model = CardIssuer
        fields = '__all__'

class CardCategorySerializer(serializers.ModelSerializer):
    credit_cards = CreditCardSerializer(many=True, read_only=True)  # Display related credit cards

    class Meta:
        model = CardCategory
        fields = '__all__'

# class CreditCardHomeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditCard
#         fields = ['id', 'name','welcome_benefit','ideal_for', 'card_image','annual_fee' , 'joining_fee ', 'rewards_type','card_upload_date']  # Include necessary fields


class PostSerializer(serializers.ModelSerializer):
    credit_cards = CreditCardSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


