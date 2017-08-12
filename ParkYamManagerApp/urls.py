"""ParkYamManagerApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
import views
from views import MessageListView
from views import UnrepliedMessageListView
from django.views.generic import TemplateView

app_name = 'app'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^roomscleaning/$', views.rooms_cleaning, name='rooms_cleaning'),
    url(r'^roomscleaning/(?P<room_number>[0-9]+)/$', views.detail, name='detail'),
    url(r'^roomscleaning/(?P<room_number>[0-9]+)/set_clean/$', views.set_clean, name='set_clean'),

    url(r'^roomsmaintenance/$', views.rooms_maintenance, name='rooms_maintenance'),
    url(r'^roomsmaintenance/(?P<room_number>[0-9]+)/$', views.room_maintenance_details, name='room_maintenance_details'),
    url(r'^roomsmaintenance/(?P<room_number>[0-9]+)/set_room_maintenance_status/$', views.set_room_maintenance_status, name='set_room_maintenance_status'),

    url(r'^roomsummary/$', views.rooms_summary, name='rooms_summary'),

    url(r'^sendmessage/$', views.send_message, name='send_message'),
    url(r'^messages/$', MessageListView.as_view(), name='messages'),
    url(r'^pending_messages/$', UnrepliedMessageListView.as_view(), name='pending_messages'),
    url(r'^reply/(?P<message_id>[0-9]+)/$', views.reply_message, name='reply'),

    url(r'^reception/$', views.reception, name = 'reception'),
	url(r'^reception/(?P<room_number>[0-9]+)/$', views.room_reception_details, name='room_reception_details'),
    url(r'^shifts/$', views.shift, name='shifts'),
    url(r'^shifts/calculate_shifts$', views.calculate_shifts, name="calculate_shifts"),
    url(r'^schedule/$', views.current_shift, name='schedule'),

    url(r'^staff', TemplateView.as_view(template_name=r'app\staff.html'),name='staff'),

]
