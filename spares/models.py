from django.db import models
from django.utils import timezone

from accounts.models import User

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.category_name

class Inventory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=False)
    quantity = models.PositiveIntegerField(default=0, blank=False, null=False)
    price = models.FloatField(null=False, blank=False)
    is_displayed = models.BooleanField(default=True)
    has_discount = models.BooleanField(default=False)
    discount = models.FloatField(blank=False, null=False, default=0)
    photo = models.ImageField(upload_to='photos/spares')
           
    class Meta:  
        verbose_name = 'inventory'
        verbose_name_plural = 'inventory'
    
    def __str__(self):
        return self.name

    @property
    def selling_price(self):
        if self.has_discount:
            return self.price - self.discount
        return self.price
    @property
    def percentage_discount(self):
        return round((self.discount/self.price)*100 ,2)
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.item)

    @property
    def item_total(self):
        return self.item.selling_price * self.quantity

    @classmethod
    def cart_count(cls, user_id):
        items = cls.objects.filter(user = user_id, is_ordered = False)
        count= sum(items.values_list('quantity', flat=True))
        return int(count)

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=50, null=False, blank=False)
    region = models.CharField(max_length=50, null=False, blank=False)
    shipping_location = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.user.email

    @property
    def shipping_fee(self):
        pass

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField("Cart")
    order_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=100, blank=False, null=False)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    delivery_date = models.DateTimeField(blank=True, null=True)
    shipping_details = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email

    @property
    def item_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.item_total
        return total

    @property
    def order_total(self):
        return self.item_total + self.shipping_fee