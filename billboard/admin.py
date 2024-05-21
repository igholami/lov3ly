from django.contrib import admin

# Register your models here.
from .models import Relationship, Participation, ImportantDate

admin.site.register(Participation)


# Fix admin site to be able to edit participants in a relationship
class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1

class importantDateInline(admin.TabularInline):
    model = ImportantDate
    extra = 1


class RelationshipAdmin(admin.ModelAdmin):
    inlines = [
        ParticipationInline,
        importantDateInline,
    ]


admin.site.register(Relationship, RelationshipAdmin)

admin.site.register(ImportantDate)