# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

from .models import Hello
from .models import ShiftForm

# Create your views here.


def home(request):
    # hello = Hello()
    # hello.comment = "dekel :)"
    # hello.days_type = 1
    # hello.times_type = 3

    if request.method == 'POST':
        hello = Hello()
        form = ShiftForm(request.POST)
        if form.is_valid():
            hello.days_type = form.cleaned_data['days_type']
            hello.times_type = form.cleaned_data['times_type']
            hello.comment = form.cleaned_data['comment']
            hello.save()
            return render(request, 'shifts/hello.html')
    else:
        pass
        form = ShiftForm()
    return render(request,"shifts/hello.html", {'form': form})
