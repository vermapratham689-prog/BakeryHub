from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Shop(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f'{self.name} — {self.shop.name}'

class Offer(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)
    discount_percent = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)])
    active = models.BooleanField(default=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.title} ({self.discount_percent}% off)'

class Order(models.Model):
    STATUS_CHOICES = [('Pending','Pending'), ('Confirmed','Confirmed'), ('Preparing','Preparing'), ('Ready','Ready for pickup'), ('Delivered','Delivered'), ('Cancelled','Cancelled')]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='bakery_orders')
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT, related_name='orders')
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    delivery_address = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Order #{self.pk} — {self.customer_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_at_purchase = models.DecimalField(max_digits=9, decimal_places=2)
    def line_total(self): return self.quantity * self.price_at_purchase

class Review(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bakery_reviews')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['customer', 'shop', 'product'], name='one_review_per_customer_shop_product')]
        ordering = ['-created_at']
    def __str__(self): return f'{self.rating}/5 by {self.customer}'
