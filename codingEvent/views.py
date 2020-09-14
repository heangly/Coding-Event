from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import *

def index(request):
  events = Event.objects.all().order_by('-postingAt')
  paginator = Paginator(events, 6)

  if request.GET.get("page"):
    try:
        events = paginator.page(request.GET.get("page"))
    except:
        events = paginator.page(1)
  else:
    events = paginator.page(1)
  return render(request, 'codingEvent/index.html', {'events': events, 'nbar': 'home'})

@login_required
def eventDetail(request, event_id):
  event = Event.objects.get(id=event_id)

  try:
    comment = Comment.objects.filter(event=event).order_by('-postingAt')
  except:
    comment = None

  try:
    attendee = Interest.objects.filter(event=event, going=True)
  except:
    attendee = None

  try:
    planner = Interest.objects.filter(event=event, planing=True)
  except:
    planner = None

  try:
    interest = Interest.objects.get(event=event, owner=request.user)
  except:
    interest = None

  return render(request, 'codingEvent/event_detail.html', {
    'event': event, 
    'interest':interest,
    'attendee': attendee,
    'planner': planner,
    'comment':comment
  })

@login_required
def createEvent(request):
  imgPlaceholder = 'https://www.worldloppet.com/wp-content/uploads/2018/10/no-img-placeholder.png'
  videoPlaceholder = '<iframe width="560" height="315" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
  if request.method == "POST":
    title = request.POST["title"]
    eventDate = request.POST["date"]
    location = request.POST["location"]
    image = request.POST["image"]
    video = request.POST["video"]

    if not image:
      image = imgPlaceholder

    if not video:
      video = videoPlaceholder

    category = request.POST["category"]
    description = request.POST["description"]

    event = Event(
      owner = request.user,
      title = title,
      image = image,
      video = video,
      category = category,
      description = description,
      location = location,
      active = True,
      startingAt = eventDate,
      seatTaken = 0
    )
    event.save()
    return HttpResponseRedirect(reverse("index"))
    
  return render(request, 'codingEvent/create_event.html', {'nbar': 'create'})

@csrf_exempt
@login_required
def interest(request):
  if request.method == "POST":
    eventId = json.loads(request.body)['eventId']
    type = json.loads(request.body)['type']
    event = Event.objects.get(id=eventId)

    try:
      exisitingInterest = Interest.objects.get(event=event, owner=request.user)
      if type == 'going':
        if exisitingInterest.going:
          exisitingInterest.going = False
          if event.seatTaken > 0:
            event.seatTaken -= 1
            event.save()

        else:
          exisitingInterest.going = True
          event.seatTaken += 1
          event.save()
        exisitingInterest.save()
        return JsonResponse({"going":exisitingInterest.going, 'seat':event.seatTaken}, status=201)
      
      elif type == 'planing':
        if exisitingInterest.planing:
            exisitingInterest.planing = False
        else:
          exisitingInterest.planing = True
        exisitingInterest.save()
        return JsonResponse({"planing":exisitingInterest.planing}, status=201)

    except:
      if type == 'going':
        event.seatTaken += 1
        event.save()
        interest = Interest(
          owner = request.user,
          event = event,
          going = True,
          planing = False,
          planingImportant=False
        )
        interest.save()
        print('new going')
        return JsonResponse({"going":interest.going, 'seat':event.seatTaken}, status=201)

      else:
        interest = Interest(
          owner = request.user,
          event = event,
          going = False,
          planing = True,
          planingImportant=False
        )
        interest.save() 
        print('new planing')
        return JsonResponse({"planing":interest.planing}, status=201)

@csrf_exempt
@login_required
def comment(request):
  if request.method == "POST":
    type = json.loads(request.body)['type']
    
    if type == 'delete':
      commentId = json.loads(request.body)['commentId']
      comment = Comment.objects.get(id=commentId);
      comment.delete()
      return JsonResponse({"delete":"success"}, status=201)
    else:
        eventId = json.loads(request.body)['eventId']
        content = json.loads(request.body)['content']
        event = Event.objects.get(id=eventId)
        newComment = Comment(owner=request.user, comment=content, event=event)
        newComment.save()
        return JsonResponse({"comment":newComment.comment, 'owner':newComment.owner.username}, status=201)

@csrf_exempt
@login_required
def active(request):
    if request.method == "POST":
      eventId = json.loads(request.body)['eventId']
      event = Event.objects.get(id=eventId)
      event.active = False
      event.save()
      return JsonResponse({"active":event.active}, status=201)

def loginView(request):
    logout(request)
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "codingEvent/login.html", {
                "message": "Invalid username and/or passwords",
                'nbar': 'home'
            })
    else:
        return render(request, "codingEvent/login.html", {'nbar': 'login'})


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    logout(request)
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "codingEvent/register.html", {
                "message": "Passwords must match"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "codingEvent/register.html", {
                "message": "Username already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "codingEvent/register.html", {'nbar': 'register'})

@csrf_exempt
@login_required
def going(request):
  if request.method == "POST":
    eventId = json.loads(request.body)['eventId']
    type = json.loads(request.body)['type']
    event = Event.objects.get(id=eventId)
    exisitingInterest = Interest.objects.get(event=event, owner=request.user)

    if type == 'cancel':
      exisitingInterest.going = False
      exisitingInterest.save()
      if event.seatTaken > 0:
        event.seatTaken -= 1
        event.save()
   
      return JsonResponse({"cancel":True}, status=201)

  else:
    goingEvent = Interest.objects.filter(owner=request.user, going=True)
    return render(request, "codingEvent/going.html", {'events':goingEvent, 'nbar': 'going'})

@csrf_exempt
@login_required
def planing(request):
  if request.method == "POST":
    eventId = json.loads(request.body)['eventId']
    type = json.loads(request.body)['type']
    event = Event.objects.get(id=eventId)
    exisitingInterest = Interest.objects.get(event=event, owner=request.user)

    if exisitingInterest.planingImportant:
      exisitingInterest.planingImportant = False
    else:
      exisitingInterest.planingImportant = True
    exisitingInterest.save()

    
    return JsonResponse({"success":True}, status=201)


  planingEvent = Interest.objects.filter(owner=request.user, planing=True)
  return render(request, "codingEvent/planing.html", {'events':planingEvent, 'nbar':'planing'})