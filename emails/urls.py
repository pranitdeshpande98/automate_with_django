from .  import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('send_email/',views.send_email,name='send_email'),
    path('track/click/<unique_id>/', views.track_click, name='track_click'),
    path('track/open/<unique_id>/', views.track_open, name='track_open'),
]