from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import (
        UserRegisterForm,
)

def register(request, *args, **kwargs):
    templates = 'users/register.html'

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for %s !' % username)
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, templates, context)
