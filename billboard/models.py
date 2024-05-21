from django.db import models
from django.contrib.auth import get_user_model


class Relationship(models.Model):
    since = models.DateTimeField()

    def __str__(self):
        if self.participants.count() == 0:
            return "Nobody"
        return " & ".join([p.user.username for p in self.participants.all()])


class Participation(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True)
    relationship = models.ForeignKey(Relationship, on_delete=models.SET_NULL, null=True, related_name='participants')

    def __str__(self):
        return f"{self.user.username if self.user else 'Nobody'} in ({self.relationship})"
