from django.contrib import admin

from apps.places.models import Place, Seat

admin.site.register([Place, Seat])
