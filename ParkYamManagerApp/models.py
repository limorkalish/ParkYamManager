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
