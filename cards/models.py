from django.db import models
from django.utils.text import slugify
from django.utils import timezone  # Import timezone for default value
import os

def card_image_upload_path(instance, filename):
    """
    Function to generate the path where the image will be stored
    inside the static/cardimg/{issuer_folder}/
    """
    # Get the issuer folder based on the slugified issuer name
    issuer_folder = slugify(instance.issuer.name)
    
    # Extract the file extension from the original filename
    file_ext = filename.split('.')[-1]
    
    # Define the new filename as the card slug with '_cc' suffix
    new_filename = f"{slugify(instance.name)}_cc.{file_ext}"
    
    # Construct the full path: static/cardimg/{issuer_folder}/{new_filename}
    return os.path.join('cardimg', issuer_folder, new_filename)



class CardIssuer(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Required
    heading = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)  # New title field

    slug = models.SlugField(max_length=255, unique=True, blank=True)
    issuer_image = models.ImageField(upload_to='issuer_images/', blank=True, null=True)
    issuer_image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    cards_image = models.ImageField(upload_to='cards_images/', blank=True, null=True)
    cards_image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    issuer_description = models.TextField(blank=True, null=True)
    cards_description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    credit_cards = models.ManyToManyField('CreditCard', related_name='issuers', blank=True)
    
    # SEO Fields
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)



    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CardIssuer, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


from django.utils.text import slugify

class CardCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    heading = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)  # New title field
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category_description = models.TextField(blank=True, null=True)
    category_image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    category_image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    cards_image = models.ImageField(upload_to='cards_images/', blank=True, null=True)
    cards_image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    cards_description = models.TextField(blank=True, null=True)
    
    # SEO Fields
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CardCategory, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    category_description = models.TextField(blank=True, null=True)
    category_image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    category_image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    cards_image = models.ImageField(upload_to='cards_images/', blank=True, null=True)
    cards_image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    cards_description = models.TextField(blank=True, null=True)
    
    # SEO Fields
    meta_title = models.CharField(max_length=120, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CardCategory, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name



class CreditCard(models.Model):
    CARD_TYPE_CHOICES = [
        ('RUPAY', 'RuPay'),
        ('VISA', 'Visa'),
        ('MASTERCARD', 'MasterCard'),
        ('AMEX', 'American Express'),
    ]

    name = models.CharField(max_length=255, unique=True)  # Ensure name is unique and required
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # Slug is optional
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, blank=True, null=True)  # Allow null values
    issuer = models.ForeignKey(CardIssuer, related_name='cr', on_delete=models.CASCADE)
    
    # Many-to-Many relation for card categories
    card_category = models.ManyToManyField(CardCategory, related_name='credit_cards')

    # Changed annual_fee and joining_fee to CharField to accept text input
    annual_fee = models.CharField(max_length=255, blank=True, null=True)
    joining_fee = models.CharField(max_length=255, blank=True, null=True)
    renewal_fee = models.CharField(max_length=255, blank=True, null=True)

    # Changed rewards_type to CharField to accept text input
    rewards_rate = models.CharField(max_length=255, blank=True, null=True)
    rewards_type = models.CharField(max_length=255, blank=True, null=True)  # Now a text field
    reward_redemption = models.TextField(blank=True, null=True)
    card_image = models.ImageField(upload_to=card_image_upload_path, blank=True, null=True)
    card_image_alt_text = models.CharField(max_length=255, blank=True, null=True)
    ideal_for = models.CharField(max_length=255, blank=True, null=True)
    welcome_benefit = models.TextField(blank=True, null=True)

    # Benefits
    movie_benefits = models.TextField(blank=True, null=True)
    dining_benefits = models.TextField(blank=True, null=True)
    travel_benefits = models.TextField(blank=True, null=True)
    domestic_lounge_access = models.TextField(blank=True, null=True)
    international_lounge_access = models.TextField(blank=True, null=True)
    golf_benefits = models.TextField(blank=True, null=True)
    insurance_benefits = models.TextField(blank=True, null=True)
    spend_based_waiver = models.TextField(blank=True, null=True)
    eligibility=models.TextField(blank=True, null=True)
    document_required=models.TextField(blank=True, null=True)
  
    # Financial Details
    foreign_currency_markup = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fuel_surcharge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cash_advance_charges = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Additional Information
    card_details = models.TextField(blank=True, null=True)
    pros = models.TextField(blank=True, null=True)
    cons = models.TextField(blank=True, null=True)

    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    apply_now_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    popular = models.BooleanField(default=False)

    # SEO Fields
    meta_title = models.CharField(max_length=120, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)

    # New Field: Card Upload Date
    card_upload_date = models.DateField(default=timezone.now)


    def save(self, *args, **kwargs):
        # Ensure slug is generated if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Save the model normally, path handling is done by card_image_upload_path
        super(CreditCard, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
 
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    conclusion = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, default='post_images/default_image.jpg')

    
    # SEO-related fields
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.CharField(max_length=255, blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    # Many-to-Many relationship with CreditCard
    credit_cards = models.ManyToManyField(CreditCard, related_name='posts')
    
    def __str__(self):
        return self.title



class FAQ(models.Model):
    issuer = models.ForeignKey(CardIssuer, related_name='related_faqs', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(CardCategory, related_name='related_faqs', on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    def __str__(self):
        return self.question