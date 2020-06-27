from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=30)
    pwd=models.CharField(max_length=100)
    email=models.CharField(max_length=30)
    salt=models.CharField(max_length=100)
    is_active=models.BooleanField(default=False)
    class Meta:
        db_table='tb_users'