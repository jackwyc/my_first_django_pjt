from django.shortcuts import render , redirect # 추가
from django.views.generic.edit import FormView # 추가
from django.views.generic import ListView # 추가
from django.utils.decorators import method_decorator # 추가
from django.db import transaction  # 추가
from user.decorators import login_required # 추가
from .forms import RegisterForm # 추가
from .models import Order # 추가
from product.models import Product
from user.models import User

# Create your views here.

@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView): # 추가
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity=form.data.get('quantity'),
                product=prod,
                user=User.objects.get(email=self.request.session.get('user'))
                )
            order.save()
            prod.stock -= int(form.data.get('quantity'))
            prod.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/product/' + str(form.data.get('product')))

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw


@method_decorator(login_required, name='dispatch')
class OrderList(ListView): # 추가
    template_name = 'order.html'
    content_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(user__email=self.request.session.get('user'))
        return queryset