from this import d
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    family_name = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)

    @property
    def total_price(self):
        return self.inovoice_set.aggregate(total_price=models.Sum('price'))['total_price']
    

    def __str__(self):
        return self.name

class Inovoice(models.Model):
    family = models.ForeignKey(User, on_delete=models.CASCADE)
    owner= models.ForeignKey(Member, on_delete=models.CASCADE)
    description = models.TextField()
    price= models.IntegerField()
    updated= models.DateTimeField(auto_now=True)
    created= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description