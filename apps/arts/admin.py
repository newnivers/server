from django.contrib import admin

from apps.arts.models import Art, ArtSchedule, Ticket

admin.site.register([Art, ArtSchedule, Ticket])
