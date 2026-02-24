from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from datetime import date
from django.contrib import messages
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

def organizer_dashboard(request):
    today = date.today()
    filter_type = request.GET.get('type', 'all')
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_participants = Participant.objects.aggregate(total=Count('id'))['total'] or 0

    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gt=today)),
        past=Count('id', filter=Q(date__lt=today)),
    )

    base_query = Event.objects.select_related('category').prefetch_related('participants')

    if search_query:
        base_query = base_query.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    
    if category_filter:
        base_query = base_query.filter(category_id=category_filter)
    if start_date and end_date:
        base_query = base_query.filter(date__range=[start_date, end_date])

    if filter_type == 'upcoming':
        events = base_query.filter(date__gt=today)
    elif filter_type == 'past':
        events = base_query.filter(date__lt=today)
    else:
        events = base_query.all()

    todays_events = Event.objects.filter(date=today).select_related('category')
    categories = Category.objects.all()

    context = {
        "events": events,
        "todays_events": todays_events,
        "counts": counts,
        "total_participants": total_participants,
        "search_query": search_query,
        "categories": categories,
        "start_date": start_date,
        "end_date": end_date,
        "today": today,
    }
    return render(request, "dashboard/organizer_dashboard.html", context)

def create_event(request):
    form = EventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Event Created Successfully")
        return redirect('organizer-dashboard')
    return render(request, "form_template.html", {"form": form, "title": "Create Event"})

def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    form = EventForm(request.POST or None, instance=event)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Event Updated Successfully")
        return redirect('organizer-dashboard')
    return render(request, "form_template.html", {"form": form, "title": "Update Event"})

def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
    return redirect('organizer-dashboard')