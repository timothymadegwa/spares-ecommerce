from django.db import models

# Create your models here.
CHOICES = (
    ('Perfume', 'Perfume'),
    ('Cosmetics', 'Cosmetics'),
)

class Inventory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100, choices=CHOICES)
    category = models.CharField(max_length=100, choices=CHOICES)
    quantity = models.PositiveIntegerField(default=0, blank=False, null=False)
    price = models.FloatField(null=False, blank=False)
    is_displayed = models.BooleanField(default=True)
    has_discount = models.BooleanField(default=False)
    discount = models.FloatField(blank=False, null=False)
    photo = models.ImageField(upload_to='photos/spares')
           
    class Meta:
            
        verbose_name = 'inventory'
        verbose_name_plural = 'inventories'
    
    def __str__(self):
        return self.name


    def total(self):
        return round(self.quantity * self.price, 2)
'''
    @property
    def quantity_sold(self):
        saleitems = self.saleitem_set.all()
        total = 0
        for item in saleitems:
            total += item.quantity_sold
'''