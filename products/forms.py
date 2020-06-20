from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        return sku.lower()
