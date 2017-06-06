# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Room
from .models import Message
from .models import SendMessageForm
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

def reception(request):
    rooms = Room.objects.all()
    rooms_by_floor = [[] for i in xrange(6)]
    for room in rooms:
        rooms_by_floor[room.floor-1].append(room)
    for rooms in rooms_by_floor:
        rooms.sort(key=lambda x:x.number)
    context = {'rooms_by_floor': rooms_by_floor}
    return render(request, 'app/reception.html', context)

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

@permission_required('ParkYamManagerApp.can_send_message')
def send_message(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        message = Message()
        message.user = request.user

        # Create a form instance and populate it with data from the request (binding):
        form = SendMessageForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            message.Message = form.cleaned_data['message']
            message.save()

            # redirect to a new URL:
            return render(request, 'app/message_sent.html')

    # If this is a GET (or any other method) create the default form.
    else:
        form = SendMessageForm()

    return render(request, 'app/send_message.html', {'form': form})