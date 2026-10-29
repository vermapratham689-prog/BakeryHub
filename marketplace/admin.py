from django.contrib import admin
from .models import Shop, Category, Product, Offer, Order, OrderItem, Review, Campaign, Coupon, MarketingEvent
admin.site.register(Shop)
admin.site.register(Category)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): list_display = ('name','shop','price','available'); list_filter = ('available','category')
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin): list_display = ('title','shop','discount_percent','active')
class OrderItemInline(admin.TabularInline): model = OrderItem; extra = 0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): list_display = ('id','customer_name','shop','total_amount','status','created_at'); list_filter = ('status','shop'); inlines = [OrderItemInline]
admin.site.register(Review)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'status', 'start_date', 'end_date', 'budget')
    list_filter = ('status', 'start_date')
    search_fields = ('name', 'shop__name')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'shop', 'discount_type', 'discount_value', 'active', 'times_used', 'usage_limit')
    list_filter = ('active', 'discount_type')
    search_fields = ('code', 'shop__name')

admin.site.register(MarketingEvent)
