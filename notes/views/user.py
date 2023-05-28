
from django.views.generic import View
from django.shortcuts import render, redirect
from notes.models import Account
from notes.forms import CustomUserCreationForm
from django.contrib import messages



class Register(View):

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        context = {
            'title' : 'Register',
            'form' : form,
        }
        template = 'registration/register.html'
        return render(request, template, context)
    
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid() :
            pengguna = form.save(commit=False)
            pengguna.is_verified = True
            pengguna.save()
            messages.success(request, 'Registration complete you can try to log in.')
            return redirect('dashboard',)
        messages.error(request, 'Registration Failed.')
        return render(request, 'registration/register.html', {'form' : form, })