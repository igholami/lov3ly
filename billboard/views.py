from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from billboard.models import Relationship


# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('fingerprint')
    user = request.user
    in_relationship = Relationship.objects.filter(participants__user=user).exists()
    relationship, partners, since, ordered_events = None, None, None, None
    admitted = False
    if in_relationship:
        relationship = user.participation.relationship
        partners = relationship.participants.exclude(pk=user.pk)
        admitted = all([p.user.profile.online for p in partners])
        since = relationship.since
        ordered_events = relationship.important_dates.order_by('date')
        fall_events = relationship.important_dates.filter(name='Fall in Love')
        if fall_events.exists():
            since = fall_events.first().date
    return render(request, 'home.html', context={
            'user': request.user,
            'in_relationship': in_relationship,
            'relationship': relationship,
            'partners': partners,
            'admitted': admitted,
            'since': since,
            'ordered_events': ordered_events,
        })
