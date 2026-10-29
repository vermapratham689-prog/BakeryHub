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


class Campaign(models.Model):
    STATUS_CHOICES = [('Draft', 'Draft'), ('Scheduled', 'Scheduled'), ('Active', 'Active'), ('Paused', 'Paused'), ('Completed', 'Completed')]
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    target_audience = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [models.CheckConstraint(condition=models.Q(end_date__gte=models.F('start_date')), name='campaign_end_after_start')]

    def __str__(self):
        return f'{self.name} — {self.shop.name}'


class Coupon(models.Model):
    DISCOUNT_TYPES = [('percent', 'Percentage'), ('fixed', 'Fixed amount')]
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=32)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, default='percent')
    discount_value = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    minimum_order = models.DecimalField(max_digits=9, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    valid_until = models.DateTimeField(blank=True, null=True)
    usage_limit = models.PositiveIntegerField(default=100)
    times_used = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['shop', 'code'], name='unique_coupon_code_per_shop')]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.code} — {self.shop.name}'


class MarketingEvent(models.Model):
    EVENT_CHOICES = [('shop_view', 'Shop view'), ('menu_view', 'Menu view'), ('campaign_click', 'Campaign click'), ('coupon_redeem', 'Coupon redemption')]
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='marketing_events')
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.get_event_type_display()} — {self.shop.name}'
