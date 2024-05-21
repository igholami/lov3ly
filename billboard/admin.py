from django.contrib import admin

# Register your models here.
from .models import Relationship, Participation

admin.site.register(Participation)


# Fix admin site to be able to edit participants in a relationship
class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1


class RelationshipAdmin(admin.ModelAdmin):
    inlines = [
        ParticipationInline,
    ]


admin.site.register(Relationship, RelationshipAdmin)
