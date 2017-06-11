# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

# Create your models here.
class Hello(models.Model):

    days = [
        (0,'Sunday'),
        (1,'Monday'),
        (2,'Tuesday'),
    ]

    times = [
        (0,'Morning'),
        (1,'Afternoon'),
        (2,'Night'),
        (3,'Off'),
        (4,'General')
    ]

    id = models.IntegerField("Shift ID", primary_key=True)
    days_type = models.IntegerField("Working day", choices=days, default='Sunday')
    times_type = models.IntegerField("Shift", choices=times, default='Morning')

    comment = models.CharField("Comment", max_length=255, default="")

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
        model = Hello
        fields = ['days_type','times_type','comment']