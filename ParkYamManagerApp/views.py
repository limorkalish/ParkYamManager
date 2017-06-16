# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Room
from .models import Message
from .models import SendMessageForm
from .models import ReceptionWorker
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views import generic
from django.utils.decorators import method_decorator
from .models import Shift
from .models import ShiftAssignment
from .models import ShiftForm
# Create your views here.

def home(request):
    return render(request,"app/home.html")

def get_rooms_floors():
    rooms = Room.objects.all()
    rooms_floors = set(map(lambda room: room.floor, rooms))
    return rooms_floors

def get_rooms_by_floor(request):
    rooms = Room.objects.all()

    rooms_floors = get_rooms_floors()

    floor_filter = 0
    try:
        floor_filter = int(request.GET.get('floor', False))
    except ValueError:
        pass

    rooms_by_floor = [[] for i in rooms_floors]
    for room in rooms:
        if floor_filter:
            if room.floor != floor_filter:
                continue
            else:
                rooms_by_floor[0].append(room)
        else:
            rooms_by_floor[room.floor - 1].append(room)
    return rooms_by_floor

@permission_required('ParkYamManagerApp.clean_room')
def rooms_summary(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'app/rooms_summary.html', context)

@permission_required('ParkYamManagerApp.clean_room')
def rooms_cleaning(request):
    rooms_by_floor = get_rooms_by_floor(request)
    number_of_floors = len(get_rooms_floors())
    context = {'rooms_by_floor': rooms_by_floor, 'number_of_floors': xrange(1, number_of_floors+1)}
    return render(request, 'app/rooms_cleaning.html', context)

@permission_required('ParkYamManagerApp.maintain_room')
def rooms_maintenance(request):
    rooms_by_floor = get_rooms_by_floor(request)
    number_of_floors = len(get_rooms_floors())
    context = {'rooms_by_floor': rooms_by_floor, 'number_of_floors': xrange(1, number_of_floors+1)}
    return render(request, 'app/rooms_maintenance.html', context)

@permission_required('ParkYamManagerApp.view_room_status')
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

@permission_required('ParkYamManagerApp.maintain_room')
def room_maintenance_details(request, room_number):
    room = get_object_or_404(Room, pk=room_number)
    return render(request, 'app/room_maintenance_details.html', {'room': room, 'comment_value':room.maintenance_comment})

@permission_required('ParkYamManagerApp.view_room_status')
def room_reception_details(request, room_number):
    room = get_object_or_404(Room, pk=room_number)
    return render(request, 'app/room_reception_details.html', {'room': room})


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
        room.is_room_being_cleaned = False
        room.save()
    elif selected_choice == "not clean":
        room.is_clean = False
        room.is_room_being_cleaned = False
        room.save()
    elif selected_choice== "in progress":
        room.is_clean = False
        room.is_room_being_cleaned = True
        room.save()
    else:
        return HttpResponse("Error 2")
    return HttpResponseRedirect(reverse('app:rooms_cleaning'))

@permission_required('ParkYamManagerApp.maintain_room')
def set_room_maintenance_status(request, room_number):
    room = Room.objects.get(number=room_number)
    try:
        selected_choice = request.POST['choice']
        maintenance_comment = request.POST['maintenance_comment']
    except KeyError:
        return render(request, 'app/room_maintenance_details.html', {
            'room': room,
            'error_message': "You didn't select a choice.",
        })
    room.maintenance_comment = maintenance_comment
    if selected_choice == "need maintenance":
        room.needs_maintenance = True
        room.save()
    elif selected_choice == "does not need maintenance":
        room.needs_maintenance = False
        room.save()
    else:
        return HttpResponse("Error 2")
    return HttpResponseRedirect(reverse('app:rooms_maintenance'))


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
            message.message = form.cleaned_data['message']
            message.save()

            # redirect to a new URL:
            return render(request, 'app/message_sent.html')

    # If this is a GET (or any other method) create the default form.
    else:
        form = SendMessageForm()

    return render(request, 'app/send_message.html', {'form': form})

class MessageListView(generic.ListView):
    model = Message
    template_name = 'app/user_messages.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).order_by('-message_time')


def shift(request):
    workers = ReceptionWorker.objects.all()
    return render(request,"app/shift.html", {'workers': workers})

def calculate_shifts(request):
    # print request.POST
    class Shift:
        def __init__(self, id, next, prev, po_list):
            self.id = id
            self.next = next
            self.prev = prev
            self.po_list = po_list[:]

    def solve_r(shifts, ac):  # assigned_counter
        if len(shifts) == 0:
            return True
        x = [len(i.po_list) for i in shifts]
        cur = shifts[x.index(min(x))]
        opts = cur.po_list
        opts.sort(key=lambda x: ac[x])
        for opt in opts:
            if cur.next and opt in cur.next.po_list:
                cur.next.po_list.remove(opt)
                was_in_next = True
            else:
                was_in_next = False

            if cur.prev and opt in cur.prev.po_list:
                cur.prev.po_list.remove(opt)
                was_in_prev = True
            else:
                was_in_prev = False
            shifts.remove(cur)
            cur.worker = opt
            ac[opt] += 1
            if solve_r(shifts, ac):
                return True
            ac[opt] -= 1
            shifts.append(cur)
            if was_in_next:
                cur.next.po_list.append(opt)
            if was_in_prev:
                cur.prev.po_list.append(opt)
        return False

    def solve(shifts, ac):
        return solve_r(shifts[:], ac)

    workers = ReceptionWorker.objects.all()
    ac = [0] * len(workers)
    shifts = [Shift(i, None, None, [j for j in xrange(len(workers)) if u"%d_%d"%(j,i) in request.POST]) for i in xrange(21)]
    for i in xrange(21):
        if i != 20:
            shifts[i].next = shifts[i + 1]
        if i != 0:
            shifts[i].prev = shifts[i - 1]

    if True == solve(shifts, ac):
        #Delete previous result
        ShiftAssignment.objects.all().delete()

        sol = [None]*21
        for s in shifts:
            sol[s.id] = ReceptionWorker.objects.get(id=s.worker).worker_name
            shift_assignment = ShiftAssignment()
            shift_assignment.id = s.id
            shift_assignment.worker_name = sol[s.id]
            shift_assignment.save()
        return render(request, "app/shift_assignment.html", {'sol': sol})
    else:
        return render(request, "app/shift_assignment_error.html")
def get_schedule(request):
    shifts = Shift.objects.all()

    times = [
        'Morning',
        'Afternoon',
        'Night',
        'OFF_Morning',
        'OFF_Afternoon',
        'OFF_Night',
        'OFF_Morning_Afternoon',
        'OFF_AftNoon_Night',
        'OFF_Morning_Night',
        'OFF_ALL_DAY',
    ]

    shift_org = {}
    shift_org[0] =[0,4,6,3]
    shift_org[1] = [1,4,5,3]
    shift_org[2] = [2,6, 5, 3]
    #
    # coms = {}
    # shifts = Shift.objects.all()
    # for obj in shifts:
    #     coms[obj.worker_name] = obj.comment

    results = {}
    for shift in range(3):
        results[shift] = {}
        results[shift][0] = set()
        results[shift][0].add(times[shift])
        for day in range(7):
            results[shift][day+1] = set()
        for item in shifts:
            if item.sunday in shift_org[shift]:
                results[shift][1].add(item.worker_name)
            if item.monday in shift_org[shift]:
                results[shift][2].add(item.worker_name)
            if item.tuesday in shift_org[shift]:
                results[shift][3].add(item.worker_name)
            if item.wednesday in shift_org[shift]:
                results[shift][4].add(item.worker_name)
            if item.thursday in shift_org[shift]:
                results[shift][5].add(item.worker_name)
            if item.friday in shift_org[shift]:
                results[shift][6].add(item.worker_name)
            if item.saturday in shift_org[shift]:
                results[shift][7].add(item.worker_name)

    return render(request, "app/schedule.html", {'results': results})

@permission_required('ParkYamManagerApp.view_room_status')
def current_shift(request):
    sol = [None] * 21
    for s in ShiftAssignment.objects.all():
        sol[s.id] = s.worker_name

    return render(request, "app/shift_assignment.html", {'sol': sol})


