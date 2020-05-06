from django.contrib import admin
from .models import Hitchspot

# admin.site.register(Hitchspot)

@admin.register(Hitchspot)
class HitchspotAdmin(admin.ModelAdmin):
    list_display = ('spot_id', 'latitude', 'longitude', 'avg_hitchability', 'avg_waiting_time', 'creation_date', 'update_date')
    list_filter = ('avg_hitchability', 'avg_waiting_time', 'creation_date', 'update_date')
    fields = [('latitude', 'longitude'), 'description', ('avg_hitchability', 'avg_waiting_time'), ('creation_date', 'update_date')]