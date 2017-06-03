# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Room
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

# Create your views here.

def home(request):
    return render(request,"app/home.html")

@permission_required('ParkYamManagerApp.change_room')
def rooms(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'app/rooms.html', context)
    # return HttpResponse("Hello, world. You're at the polls index.")

@permission_required('ParkYamManagerApp.change_room')
def detail(request, room_number):
    room = get_object_or_404(Room, pk=room_number)
    return render(request, 'app/detail.html', {'room': room, 'comment_value':room.clean_comment})

@permission_required('ParkYamManagerApp.change_room')
def set_clean(request, room_number):
    room = Room.objects.get(number=room_number)
    try:
        selected_choice = request.POST['choice']
        clean_comment = request.POST['clean_comment']
    except KeyError:
        return render(request, 'app/detail.html', {
            'room': room,
            'error_message': "You didn't select a choice.",
        })
    room.clean_comment = clean_comment
    if selected_choice == "clean":
        room.is_clean = True
        room.save()
    elif selected_choice == "not clean":
        room.is_clean = False
        room.save()
    else:
        return HttpResponse("Error 2")
    return HttpResponseRedirect(reverse('app:home'))