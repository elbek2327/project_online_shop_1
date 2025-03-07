from django import forms
from shop.models import Product, Category, Comment
from .models import Order
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class ProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=14, decimal_places=2)
    image = forms.ImageField(required=False)
    quantity = forms.IntegerField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    discount = forms.IntegerField(required=False, min_value=0, max_value=100)

    
    def save(self, commit=True):
        cd = self.cleaned_data
        product = None
        if commit:
            product = Product.objects.create(
                name=cd.get('name'),
                description=cd.get('description'),
                price=cd.get('price'),
                image=cd.get('image'),
                quantity=cd.get('quantity'),
                category=cd.get('category'),
                discount=cd.get('discount'),
                rating=cd.get('rating')
            )
        return product
        


class ProductModelForm(forms.ModelForm):
    
    class Meta:
        model = Product
        exclude = ()

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'surname', 'phone', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }
        


    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if self.product_id is None:
            raise ValidationError("Product ID is required for order validation.")

        product = get_object_or_404(Product, id=self.product_id)

        if quantity > product.quantity:
            raise ValidationError("Not enough stock available.")

        return quantity


# added new
class CommentForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '⭐'), #rating uchun sticker qoshdim agar '' ichda nima bolsa osha inputda korinadi
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐')
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, required=False)
    class Meta:
        model = Comment
        fields = ('commenter_name', 'comment', 'rating')
        widgets = {
            'commenter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'})
        }


