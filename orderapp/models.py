from django.db import models

# Create your models here.
class City(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField(null=True)
    cityname = models.CharField(max_length=255,null=True)
    type = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'city'
