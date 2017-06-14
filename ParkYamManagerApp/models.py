# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.core.exceptions import ValidationError

# Create your models here.

class Room(models.Model):
    number = models.IntegerField("Room Number", primary_key = True)
    floor = models.IntegerField("Room Floor")
    room_size = models.IntegerField("Room Size (Square Meter)")
    bathroom_size = models.IntegerField("Bathroom Size (Square Meter)")
    double_beds_count = models.IntegerField("Double Beds Count", default = 1)
    single_beds_count = models.IntegerField("Single Beds Count",default = 0)

    BATHROOM_TYPE = (
        (0, 'Bathtub'),
        (1, 'Shower'),
    )

    bathroom_type = models.IntegerField("Bathroom Type", choices = BATHROOM_TYPE, default = 'Shower')

    is_suite = models.BooleanField("Suite", default = False)
    is_seaview = models.BooleanField("Sea View", default = False)
    is_place_for_crib = models.BooleanField("Has Place For Crib", default = True)
    is_clean = models.BooleanField("Clean", default=True)
    clean_comment = models.CharField("Clean_comment",max_length=1000,default="")
    is_room_being_cleaned = models.BooleanField("Is Room Being Cleaned", default=False)

    needs_maintenance = models.BooleanField("NeedsMaintenance", default=False)
    maintenance_comment = models.CharField("MaintenanceComment", max_length=1000, default="")

    class Meta:
        permissions = (
            ("maintain_room", "Can maintain room"),
        )

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField("Message", default="")
    reply = models.TextField("Reply", default="", blank=True)
    replier_name = models.CharField("Replier", max_length = 255, default="", blank=True)
    message_time = models.DateTimeField("Message Time", auto_now=True)

    class Meta:
        permissions = (("can_send_message", "Can send message"), ("can_reply_message", "Can reply message"))

    def __str__(self):
        return '%s   %s   %s' % (self.user, self.message_time.strftime('%d-%m-%Y %H:%M:%S'), self.message[:20])

class SendMessageForm(ModelForm):
    def clean_message(self):
        data = self.cleaned_data['message']

        #Check message is not empty
        if not data:
            raise ValidationError('Message cannot be empty')

        return data

    class Meta:
        model = Message
        fields = ['message']
        #help_texts = {'message': ('Enter a message'), }

times = [
    (0, 'OFF_Morning'),
    (1, 'OFF_Afternoon'),
    (2, 'OFF_Night'),
    (3, 'Off_ALL_DAY'),
    (4, 'Off_Morning_Afternoon'),
    (5, 'Off_AftNoon_Night'),
    (6, 'Off_Morning_Night'),
    (7, 'General'),
]

days = [
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday')
]


class Shift(models.Model):

    id = models.IntegerField("id", primary_key=True)
    worker_name = models.CharField("Name", max_length=255, default="Type your name in here")
    sunday = models.IntegerField("Sunday", choices=times, default='7')
    monday = models.IntegerField("Monday", choices=times, default='7')
    tuesday = models.IntegerField("Tuesday", choices=times, default='7')
    wednesday = models.IntegerField("Wednesday", choices=times, default='7')
    thursday = models.IntegerField("Thursday", choices=times, default='7')
    friday = models.IntegerField("Friday", choices=times, default='7')
    saturday = models.IntegerField("Saturday", choices=times, default='7')

    comment = models.CharField("Comment", max_length=255, default="Type here any comments")

    # class Meta:
    #     permissions = (("can_send_message", "Can send message"), ("can_reply_message", "Can reply message"))

    def __str__(self):
        return '%d' % (self.id)


class ShiftForm(ModelForm):
    def clean_message(self):
        data = self.cleaned_data['hello']

        #Check message is not empty
        if not data:
            raise ValidationError('Form cannot be empty')

        return data

    class Meta:
        model = Shift
        fields = ['worker_name','sunday','monday','tuesday','wednesday','thursday','friday','saturday','comment']