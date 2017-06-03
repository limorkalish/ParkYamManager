# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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
