from django.db import models
from datetime import datetime
from django.urls import reverse
from staff.models import CustomUserModel
from django_currentuser.middleware import get_current_user,get_current_authenticated_user
from django_currentuser.db.models import CurrentUserField

def get_default_datetime():
    now = datetime.now().strftime("%b.%d,%Y %H:%M:%S")
    return now


class OSModel(models.Model):
    """Model for Operation systems"""
    op_system = models.CharField(max_length=30, blank=False)

    def __str__(self) -> str:
        return self.op_system


class FactoryModel(models.Model):
    """Model for Factory names"""
    factory_name = models.CharField(max_length=30, blank=False)

    def __str__(self) -> str:
        return self.factory_name


class InventoryModel(models.Model):
    """Maim Model with invetory"""
    qrcode = models.ImageField(upload_to='qr_codes', null=True, blank=True)
    username = models.CharField(max_length=30, default="office")
    type_chs = (
        ('Laptop', 'Laptop'),
        ('Phone', 'Phone'),
        ('Monitor', 'Monitor'),
        ('Other', 'Other'),
    )
    type_name = models.CharField(max_length=30, choices=type_chs, null=True)
    factory_name = models.ForeignKey(FactoryModel, blank=True, null=True, on_delete=models.SET_NULL)
    model_name = models.CharField(max_length=30, blank=True)
    op_system = models.ForeignKey(OSModel, blank=True, null=True, on_delete=models.SET_NULL)
    cpu_capacity = models.CharField(max_length=30, blank=True)
    ram_capacity = models.CharField(max_length=30, blank=True)
    ssd_capacity = models.CharField(max_length=30, blank=True)
    serial_number = models.CharField(max_length=30, blank=True)
    status_choice = (
        ('Free', 'Free'),
        ('Used', 'Used'),
        ('Broken', 'Broken'),
        ('Stored', 'Stored'),
        ('Sold', 'Sold'),
        ('Decommis', 'Decommis')
    )
    status = models.CharField(max_length=30, choices=status_choice)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    created_by = CurrentUserField(related_name='created_by')
    updated_by = CurrentUserField(on_update=True,related_name='updated_by')
    price_buy = models.IntegerField(default=0, null=True, blank=True)
    price_today = models.IntegerField(default=0, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)

    def get_absolute_url(self):  # new
        return reverse('inventory_details', kwargs={'pk': self.pk})
