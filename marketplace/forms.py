from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Shop, Product, Offer, Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('customer','Customer'), ('shop','Bakery owner')])
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit: user.save()
        return user

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'address', 'phone', 'logo']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image', 'available']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'discount_percent', 'active', 'ends_at']
        widgets = {'ends_at': forms.DateTimeInput(attrs={'type':'datetime-local'}, format='%Y-%m-%dT%H:%M')}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {'rating': forms.Select(choices=[(5,'5 - Excellent'),(4,'4 - Very good'),(3,'3 - Good'),(2,'2 - Fair'),(1,'1 - Poor')]), 'comment': forms.Textarea(attrs={'rows': 3, 'placeholder':'Share your experience'})}
