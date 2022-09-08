from django.db import models

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
'''
    @property
    def quantity_sold(self):
        saleitems = self.saleitem_set.all()
        total = 0
        for item in saleitems:
            total += item.quantity_sold
'''
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email