from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=50)
    sku = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Product)
def my_handler(sender, instance, created, **kwargs):
    if created:
        print("Web hooks to be triggered on creation.")
    else:
        print("Web hook to be triggered on update.")
