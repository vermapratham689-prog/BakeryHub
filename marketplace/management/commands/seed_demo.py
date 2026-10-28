from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketplace.models import Shop, Category, Product, Offer

class Command(BaseCommand):
    help = 'Create sample bakery accounts, products, and an offer for a college demonstration.'

    def handle(self, *args, **options):
        owner, _ = User.objects.get_or_create(username='demo_baker', defaults={'email':'baker@example.test'})
        owner.set_password('BakeryDemo123!')
        owner.save()
        shop, _ = Shop.objects.get_or_create(owner=owner, defaults={
            'name':'Sweet Crumbs Bakery',
            'description':'Small-batch cakes, cupcakes and pastries made fresh for every celebration.',
            'address':'Model Town, Ludhiana', 'phone':'9876543210'
        })
        categories = {}
        for name, slug in [('Cakes','cakes'),('Cupcakes','cupcakes'),('Pastries','pastries'),('Cookies','cookies')]:
            categories[name], _ = Category.objects.get_or_create(name=name, defaults={'slug':slug})
        products = [
            ('Chocolate Truffle Cake','Rich chocolate sponge with smooth ganache.',Decimal('650.00'),'Cakes'),
            ('Strawberry Celebration Cake','Soft vanilla cake with strawberry cream.',Decimal('750.00'),'Cakes'),
            ('Vanilla Cupcake Box','A box of six classic vanilla cupcakes.',Decimal('300.00'),'Cupcakes'),
            ('Chocolate Fudge Pastry','A layered pastry for a little chocolate break.',Decimal('120.00'),'Pastries'),
            ('Butter Cookies','Crunchy, buttery cookies baked in small batches.',Decimal('180.00'),'Cookies'),
        ]
        for name, description, price, category in products:
            Product.objects.get_or_create(shop=shop, name=name, defaults={
                'description':description, 'price':price, 'category':categories[category], 'available':True
            })
        Offer.objects.get_or_create(shop=shop, title='Sweet Start Offer', defaults={
            'description':'Enjoy a little celebration for less on selected bakery favourites.',
            'discount_percent':15, 'active':True
        })
        customer, _ = User.objects.get_or_create(username='demo_customer', defaults={'email':'customer@example.test'})
        customer.set_password('CustomerDemo123!')
        customer.save()
        self.stdout.write(self.style.SUCCESS('Demo data ready.'))
        self.stdout.write('Bakery owner: demo_baker / BakeryDemo123!')
        self.stdout.write('Customer: demo_customer / CustomerDemo123!')
        self.stdout.write('These are demonstration credentials only. Change them before any public deployment.')
