from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('fingerprint')
    user = request.user
    in_relationship = user.participation and user.participation.relationship
    relationship, partners = None, None
    admitted = False
    if in_relationship:
        relationship = user.participation.relationship
        partners = relationship.participants.exclude(pk=user.pk)
        admitted = all([p.user.profile.online for p in partners])
    return render(request, 'home.html', context={
            'user': request.user,
            'in_relationship': in_relationship,
            'relationship': relationship,
            'partners': partners,
            'admitted': admitted,
        })
