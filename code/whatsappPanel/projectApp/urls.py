from django.urls import path
#now import the views.py file into this code
from . import views 
urlpatterns=[
  path('', views.base, name='base'),
  path('tour_page/whatsapp_automation/', views.whatsapp_automation, name='whatsapp_automation'),
  path('tour_page/whatsapp_automation_img_and_message/', views.whatsapp_automation_img_and_message, name='whatsapp_automation_img_and_message'),
  path('tour_page/whatsapp_automation_img/', views.whatsapp_automation_img, name='whatsapp_automation_img'),
  path('tour_page/', views.tour_page, name='tour_page'),
  
]