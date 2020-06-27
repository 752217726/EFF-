from django.db import models

# Create your models here.
class Employees(models.Model):
    name=models.CharField(max_length=30)
    sex=models.CharField(max_length=30)
    age=models.IntegerField()
    tel=models.CharField(max_length=30)
    position=models.CharField(max_length=30)
    class Meta:
        db_table='tb_employees'

class ReturnSale(models.Model):
    name=models.CharField(max_length=30)
    data=models.DateTimeField()
    num = models.IntegerField(null=False)
    address = models.CharField(max_length=80)
    content = models.TextField()
    class Meta:
        db_table='tb_returnsale'

class GoodCate(models.Model):
    good_cate_name=models.CharField(max_length=30)
    parent_id=models.IntegerField()
    level=models.IntegerField()
    class Meta:
        db_table='tb_goodcate'

class Good(models.Model):
    name = models.CharField(max_length=30, null=False)
    good_name = models.CharField(max_length=30, null=False)
    date = models.DateTimeField(null=False)
    content = models.TextField(null=False)
    sell_num = models.IntegerField(null=False)
    good_id = models.ForeignKey(to=GoodCate, on_delete=models.DO_NOTHING, null=False)
    class Meta:
        db_table = 'tb_good'

class Purchase_records(models.Model):
    name=models.CharField(max_length=30)
    data=models.DateTimeField()
    num=models.IntegerField(null=False)
    address=models.CharField(max_length=80)
    content=models.TextField()
    class Meta:
        db_table='tb_purchase_records'