from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, BookingForm
from django.contrib import messages
from .models import Event, Booking
from django.db.models import Q
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('home') #it was dashboard before
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

############################################################

def dashboard(request):
    if request.user.is_anonymous:
        return redirect('login')

    now = timezone.now()
    events = Event.objects.filter(organizer= request.user)
    events_I_attended = request.user.booking_set.filter(event__date__lte=now.date(),  event__time__lte=now.today().time())

    query = request.GET.get('q')
    if query:
    
        events = events.filter(
        Q(title__icontains=query)|
        Q(description__icontains=query)
        ).distinct()

    context = {
       "events": events,
       "events_I_attended": events_I_attended,
    }
    return render(request, 'dashboard.html', context)

def event_create(request):
    if request.user.is_anonymous:
        return redirect('login')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('dashboard')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)

    attendees= Booking.objects.filter(event=event)

    context = {
        "event": event,
        "attendees":attendees,
    }
    return render(request, 'detail.html', context)

def event_edit(request, event_id):
    event = Event.objects.get(id=event_id)

    if not (request.user == event.organizer):
        return redirect('no-access')

    form = EventForm(instance=event)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        "event": event,
        "form":form,
    }
    return render(request, 'edit.html', context)

def events(request): 
    now = timezone.now()
    events = Event.objects.filter(date__gte=now).order_by('date')

    query = request.GET.get('q')
    if query:
    
        events = events.filter(
        Q(title__icontains=query)|
        Q(description__icontains=query)|
        Q(organizer__username__icontains=query)
        ).distinct()

    
    context = {
       "events": events,
    }
    return render(request, 'events.html', context)



def event_delete(request, event_id):
    event = Event.objects.get(id=event_id)

    if not (request.user == event.organizer):
        return redirect('no-access')

    event.delete()

    return redirect('home')


def event_book(request, event_id):
    event = Event.objects.get(id=event_id)
    form = BookingForm()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booked = form.save(commit=False)
            booked.user = request.user
            booked.event = event

            if booked.tickets <= event.get_remaining_seats():
                booked.save()
                messages.success(request, "You have successfully booked tickets.")
                return redirect('events')

            elif event.get_remaining_seats() == 0:
                messages.warning(request, "Event Is Full! ")
                return redirect('events')

            else:
                messages.warning(request, "No enough empty seats! There are "+str(event.get_remaining_seats())+" seats left!")
                return redirect('detail', event_id=event.id)

    context = {
        "event": event,
        "form":form,
    }

    return render(request, 'book.html', context)

def no_access(request):
    return render(request, 'no_access.html')



















