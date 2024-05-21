from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class WebauthnRegistration(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    challenge = models.CharField(max_length=9000, blank=True, null=True)

    def __str__(self):
        return self.user.email


class WebauthnAuthentication(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    challenge = models.CharField(max_length=9000, blank=True, null=True)

    def __str__(self):
        return self.user.email


class WebauthnCredentials(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="webauthn"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Name",
        blank=True,
        null=True,
    )
    credential_public_key = models.CharField(max_length=9000, blank=True, null=True)
    credential_id = models.CharField(max_length=9000, blank=True, null=True)
    current_sign_count = models.IntegerField(default=0)

    def __str__(self):
        return "Unknown" if not self.name else self.name
