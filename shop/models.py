from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64)
    picture = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    picture = models.CharField(max_length=32)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    new = models.BooleanField(default=False)
    available = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

class Order(models.Model):
    phone = models.CharField(max_length=16)
    email = models.EmailField(max_length=64)
    items = models.JSONField(max_length=128)
