from django.utils import timezone


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            request.user.profile.last_activity = now
            request.user.profile.save(update_fields=['last_activity'])
        response = self.get_response(request)
        return response
