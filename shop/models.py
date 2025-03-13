from django.db import models
from decimal import Decimal
from django.conf import settings

from django.db.models import Avg #aggregate avg ni oldim



# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    my_order = models.PositiveIntegerField(default=0,null=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'Categories'
        ordering = ['-id']



class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True, blank=True, default='images/no_image.png')
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    @property
    def discounted_price(self):
        if self.discount > 0:
            self.price = self.price * Decimal(1 - self.discount / 100)
        return Decimal(f'{self.price}').quantize(Decimal('0.00'))

    @property
    def get_absolute_url(self):
        return self.image.url
    
    def get_related_products(self):
        return Product.objects.filter(category=self.category).exclude(id=self.id)[:5]

    def avg_rating(self):
        avg = self.comments.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else None

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        ordering = ['my_order']






# order name, quantity, who is ordering, foreign key
class Order(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #qaysi productni aynan
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  #kim placed qildi
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=55)
    phone = models.CharField(max_length=14)
    quantity = models.PositiveBigIntegerField(default=1)
    is_placed = models.BooleanField(default=False) #Joylanganmi yoqmi
    
    def __str__(self):
        return f'Order: {self.product.name} - {self.quantity}'
    
    class Meta:
        db_table = 'Order'
        


# COmment  added new  migrated
class Comment(BaseModel):
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=70)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default = 0)
    def __str__(self):
        return f" {self.product.name} - {self.commenter_name}"
    

