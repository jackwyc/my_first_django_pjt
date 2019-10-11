from django.shortcuts import render, redirect # 추가
from django.views.generic.edit import FormView # 추가
from django.contrib.auth.hashers import make_password # 추가
from .forms import RegisterForm, LoginForm # 추가
from .models import User # 추가

# Create your views here.


def index(request): # 추가
    return render(request, 'index.html', {'email': request.session.get('user')})

class RegisterView(FormView): # 추가
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            email = form.data.get('email'),
            password = make_password(form.data.get('password')),
            level = 'user'
        )
        user.save()

        return super().form_valid(form)

class LoginView(FormView): # 추가
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')