from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q, Avg, Count, Sum
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import RegisterForm, ShopForm, ProductForm, OfferForm, ReviewForm
from .models import Shop, Product, Category, Offer, Order, OrderItem, Review


def home(request):
    products = Product.objects.filter(available=True).select_related('shop','category')[:8]
    offers = Offer.objects.filter(active=True).filter(Q(ends_at__isnull=True) | Q(ends_at__gte=timezone.now())).select_related('shop')[:4]
    return render(request, 'marketplace/home.html', {'products': products, 'offers': offers, 'shops_count': Shop.objects.count()})


def register(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['role'] == 'shop':
                Shop.objects.create(owner=user, name=f"{user.username}'s Bakery")
            login(request, user)
            messages.success(request, 'Account created. Welcome to BakeryHub!')
            return redirect('dashboard')
    else: form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def shops(request):
    query = request.GET.get('q','').strip()
    shop_list = Shop.objects.annotate(avg_rating=Avg('reviews__rating'), product_count=Count('products', distinct=True))
    if query: shop_list = shop_list.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(address__icontains=query))
    return render(request, 'marketplace/shops.html', {'shops': shop_list, 'query': query})


def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop.objects.select_related('owner'), pk=shop_id)
    products = shop.products.filter(available=True).select_related('category')
    offers = shop.offers.filter(active=True).filter(Q(ends_at__isnull=True) | Q(ends_at__gte=timezone.now()))
    reviews = shop.reviews.select_related('customer','product')
    return render(request, 'marketplace/shop_detail.html', {'shop':shop,'products':products,'offers':offers,'reviews':reviews,'avg_rating':reviews.aggregate(a=Avg('rating'))['a']})


def owner_shop(user):
    try: return user.shop
    except Shop.DoesNotExist: return None

@login_required
def dashboard(request):
    shop = owner_shop(request.user)
    if shop:
        orders = shop.orders.prefetch_related('items__product').order_by('-created_at')
        context = {'shop':shop,'products':shop.products.all(),'orders':orders[:10], 'order_count':orders.count(), 'sales':orders.exclude(status='Cancelled').aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00'), 'offers':shop.offers.all()}
        return render(request, 'marketplace/dashboard.html', context)
    customer_orders = request.user.bakery_orders.select_related('shop').order_by('-created_at')
    return render(request, 'marketplace/customer_dashboard.html', {'orders':customer_orders[:10], 'order_count':customer_orders.count()})

@login_required
def shop_profile(request):
    shop = owner_shop(request.user)
    if not shop: return HttpResponseForbidden('Only bakery owners can edit a shop profile.')
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid(): form.save(); messages.success(request,'Shop profile saved.'); return redirect('dashboard')
    else: form = ShopForm(instance=shop)
    return render(request, 'marketplace/form_page.html', {'form':form,'title':'Edit bakery profile','button':'Save profile'})

@login_required
def product_add(request):
    shop = owner_shop(request.user)
    if not shop: return HttpResponseForbidden('Only bakery owners can add products.')
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False); product.shop = shop; product.save(); messages.success(request,'Product added.'); return redirect('dashboard')
    return render(request,'marketplace/form_page.html',{'form':form,'title':'Add a product','button':'Save product'})

@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    if product.shop.owner_id != request.user.id: return HttpResponseForbidden('You cannot edit another shop\'s product.')
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid(): form.save(); messages.success(request,'Product updated.'); return redirect('dashboard')
    return render(request,'marketplace/form_page.html',{'form':form,'title':'Edit product','button':'Update product'})

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    if product.shop.owner_id != request.user.id: return HttpResponseForbidden('You cannot delete another shop\'s product.')
    if request.method == 'POST': product.delete(); messages.success(request,'Product deleted.')
    return redirect('dashboard')

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product,pk=product_id,available=True)
    cart = request.session.get('cart', {})
    key = str(product_id); cart[key] = int(cart.get(key,0)) + 1
    request.session['cart'] = cart
    messages.success(request,f'{product.name} added to your cart.')
    return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart')

@login_required
def cart_update(request, product_id):
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        try: quantity = int(request.POST.get('quantity','1'))
        except ValueError: quantity = 1
        if quantity <= 0: cart.pop(str(product_id),None)
        else: cart[str(product_id)] = min(quantity, 99)
        request.session['cart'] = cart
    return redirect('cart')

def cart_data(request):
    cart = request.session.get('cart', {})
    items, total = [], Decimal('0.00')
    for product_id, quantity in cart.items():
        product = Product.objects.filter(pk=product_id, available=True).select_related('shop').first()
        if not product: continue
        quantity = max(1, min(int(quantity),99)); line = product.price * quantity
        items.append({'product':product,'quantity':quantity,'line_total':line}); total += line
    return items,total

@login_required
def cart(request):
    items,total = cart_data(request)
    return render(request,'marketplace/cart.html',{'items':items,'total':total})

@login_required
def checkout(request):
    items,total = cart_data(request)
    if not items: messages.info(request,'Your cart is empty.'); return redirect('shops')
    shop_ids = {i['product'].shop_id for i in items}
    if len(shop_ids) > 1:
        messages.error(request,'For this project version, place one order per bakery. Remove products from other bakeries and try again.')
        return redirect('cart')
    if request.method == 'POST':
        name = request.POST.get('customer_name','').strip(); phone = request.POST.get('phone','').strip(); address = request.POST.get('delivery_address','').strip(); notes = request.POST.get('notes','').strip()
        if not name or not phone or not address:
            messages.error(request,'Name, phone and delivery address are required.')
            return render(request,'marketplace/checkout.html',{'items':items,'total':total})
        with transaction.atomic():
            shop = items[0]['product'].shop
            order = Order.objects.create(customer=request.user,shop=shop,customer_name=name,phone=phone,delivery_address=address,notes=notes,total_amount=total)
            for item in items: OrderItem.objects.create(order=order,product=item['product'],quantity=item['quantity'],price_at_purchase=item['product'].price)
        request.session['cart'] = {}
        messages.success(request,f'Order #{order.id} placed successfully!')
        return redirect('orders')
    return render(request,'marketplace/checkout.html',{'items':items,'total':total})

@login_required
def orders(request):
    shop = owner_shop(request.user)
    if shop: order_list = shop.orders.prefetch_related('items__product').order_by('-created_at')
    else: order_list = request.user.bakery_orders.select_related('shop').prefetch_related('items__product').order_by('-created_at')
    return render(request,'marketplace/orders.html',{'orders':order_list})

@login_required
def order_status(request, order_id):
    order = get_object_or_404(Order,pk=order_id)
    if not order.shop.owner_id == request.user.id: return HttpResponseForbidden('Only the bakery owner can update this order.')
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES): order.status = new_status; order.save(update_fields=['status']); messages.success(request,'Order status updated.')
    return redirect('orders')

@login_required
def add_review(request, shop_id):
    shop = get_object_or_404(Shop,pk=shop_id)
    eligible = Order.objects.filter(customer=request.user,shop=shop).exclude(status='Cancelled').exists()
    if not eligible:
        messages.error(request,'Place an order from this bakery before reviewing it.'); return redirect('shop_detail',shop_id=shop.id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review, created = Review.objects.update_or_create(customer=request.user,shop=shop,product=None,defaults={'rating':form.cleaned_data['rating'],'comment':form.cleaned_data['comment']})
        messages.success(request,'Thank you for your review!'); return redirect('shop_detail',shop_id=shop.id)
    return render(request,'marketplace/form_page.html',{'form':form,'title':f'Review {shop.name}','button':'Submit review'})

@login_required
def offer_add(request):
    shop = owner_shop(request.user)
    if not shop: return HttpResponseForbidden('Only bakery owners can manage offers.')
    form = OfferForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        offer = form.save(commit=False); offer.shop = shop; offer.save(); messages.success(request,'Offer published.'); return redirect('dashboard')
    return render(request,'marketplace/form_page.html',{'form':form,'title':'Create special offer','button':'Publish offer'})

@login_required
def offer_toggle(request, offer_id):
    offer = get_object_or_404(Offer,pk=offer_id)
    if offer.shop.owner_id != request.user.id: return HttpResponseForbidden('You cannot edit another shop\'s offer.')
    if request.method == 'POST': offer.active = not offer.active; offer.save(update_fields=['active'])
    return redirect('dashboard')
