# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'dojo_secrets_2_app/index.html')

def secrets(request):
    return render(request, 'dojo_secrets_2_app/secrets.html')

def register(request):
    postData = {
        "first_name" : request.POST['first_name'],
        "last_name" : request.POST['last_name'],
        "email" : str(request.POST['email']),
        "dob" : request.POST['dob'],
        "password" : request.POST['password'],
        "conpass" : request.POST['conpass']
    }
    print postData['dob']
    new_user = User.objects.register(postData)
    print new_user

    if len(new_user) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['first_name'] = postData['first_name']
        return redirect('/secrets')
    else:
        for error in new_user:
            messages.info(request, error)
    return redirect('/')

def login(request):
    postData = {
        "email" : request.POST['email'],
        "password" : request.POST['password'],
    }
    login_validation = User.objects.login(postData)

    if len(login_validation) == 0:
        request.session['id'] = User.objects.get(email=postData['email']).id
        request.session['first_name'] = User.objects.get(email=postData['email']).first_name
        return redirect('/secrets')


    for error in login_validation:
        messages.info(request, error)
        print "something happened"
        return redirect('/')
