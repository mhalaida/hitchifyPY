from django.db import models

class Hitchspot(models.Model):
    spot_id = models.AutoField(primary_key = True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    avg_hitchability = models.FloatField()
    avg_waiting_time = models.FloatField()
    creation_date = models.DateField()
    update_date = models.DateField(blank=True, null=True)

    # TODO country_id = models.IntegerField()
    # TODO user_id = models.IntegerField()