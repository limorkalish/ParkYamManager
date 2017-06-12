# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

from .models import Shift
from .models import ShiftForm

# Create your views here.


def home(request):
    # hello = Hello()
    # hello.comment = "dekel :)"
    # hello.days_type = 1
    # hello.times_type = 3

    if request.method == 'POST':
        hello = Shift()
        form = ShiftForm(request.POST)
        if form.is_valid():
            hello.days_type = form.cleaned_data['days_type']
            hello.times_type = form.cleaned_data['times_type']
            hello.comment = form.cleaned_data['comment']
            hello.save()
            return render(request, 'shifts/shift.html')
    else:
        pass
        form = ShiftForm()
    return render(request,"shifts/shift.html", {'form': form})

def get_schedule(request):
    shifts = Shift.objects.all()

    times = [
        'Morning',
        'Afternoon',
        'Night',
        'Off',
        'General'
    ]

    results = {}
    for shift in range(3):
        results[shift] = {}
        results[shift][0] = set()
        results[shift][0].add(times[shift])
        for day in range(7):
            results[shift][day+1] = set()
            for item in shifts:
                if item.days_type == day and item.times_type == shift:
                    results[shift][day+1].add(item.worker_name)

    return render(request, "shifts/schedule.html", {'results': results})