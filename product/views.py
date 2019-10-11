from django.shortcuts import render
from django.views.generic import ListView, DetailView # 추가
from django.views.generic.edit import FormView # 추가
from django.utils.decorators import method_decorator # 추가
from rest_framework import generics # 추가
from rest_framework import mixins
from .models import Product # 추가
from .forms import RegisterForm # 추가
from order.forms import RegisterForm as OrderForm # 추가
from user.decorators import admin_required # 추가
from .serializers import ProductSerializer

# Create your views here.

class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ProductList(ListView): # 추가
    model = Product
    template_name = 'product.html'
    content_object_name = 'product_list'

@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView): # 추가
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()
        return super().form_valid(form)


class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request)
        return context