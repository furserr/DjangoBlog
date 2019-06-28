from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.

def register(request):
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        user.set_password()
        user.save()
        user = authenticate(username= username, password= password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, '<b>Tebrikler kaydınız başarıyla gerçekleşti</b>', extra_tags='success')
                return HttpResponseRedirect(reverse('post-list'))

    return render(request, 'auth/register.html', context={'form': form})
