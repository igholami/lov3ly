from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from billboard.models import Relationship


# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('fingerprint')
    user = request.user
    in_relationship = Relationship.objects.filter(participants__user=user).exists()
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
