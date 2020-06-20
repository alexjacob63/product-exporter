import tempfile
import time

from django.db.models import Q
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Product
from .tasks import handle_file_upload


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 20
    ordering = ['-id']

    def get_queryset(self):
        query_set = super(ProductListView, self).get_queryset()
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            lookups = Q(name__icontains=query) | Q(sku__icontains=query)
            query_set = query_set.filter(lookups)
        return query_set


class ProductCreateView(CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_add.html'

    def get_success_url(self):
        return reverse('home')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_view.html'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_add.html'
    fields = ["name", "description", "active"]

    def get_success_url(self):
        return reverse('home')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_delete.html'

    def get_success_url(self):
        return reverse('home')


class ProductDeleteAll(DeleteView):
    model = Product
    template_name = 'product_delete_all.html'

    def get_object(self):
        if self.request.method != "GET":
            return self.model.objects.all()
        return None

    def get_success_url(self):
        return reverse('home')


def simple_upload(request):
    if request.method == 'POST' and request.FILES.get('myFile'):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["myFile"].chunks():
                f.write(chunk)
        handle_file_upload.delay(f.name)
        return redirect(reverse('home'))
    return render(request, 'simple_upload.html')


def stream(request):
    def event_stream():
        import json
        while True:
            with open('my_status.txt', 'r') as json_file:
                value = json.loads(json_file.read())
                time.sleep(3)
                if not value.get('processing'):
                    continue
                current_count = Product.objects.count()
                initial_count = value['initial_products']
                products_added = current_count - initial_count
                target = value['new_products']
                yield 'data: Added %s out of %s\n\n' % (products_added, target)
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
