from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('register', views.register, name="register"),
  path('login', views.loginView, name="login"),
  path('logout', views.logoutView, name="logout"),
  path('create_event', views.createEvent, name="create_event"),
  path('event_detail/<int:event_id>', views.eventDetail, name="event_detail"),
  path('interest', views.interest, name="interest"),
  path('active', views.active, name="active"),
  path('comment', views.comment, name="active"),
  path('going', views.going, name="going"),
  path('planing', views.planing, name="planing"),
]