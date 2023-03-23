from django.db import models
from datetime import datetime
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import qrcode
from django.conf import settings
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

class MainDomain(models.Model):
    """Model for Factory names"""
    domain_name = models.CharField(max_length=40, blank=False)

    def __str__(self) -> str:
        return self.factory_name

class InventoryModel(models.Model):
    """Maim Model with invetory"""
    qrcode = models.ImageField(upload_to='qr_codes', null=True, blank=True)
    username = models.CharField(max_length=60, default="office")
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
    def save(self, *args, **kwargs):
        is_create = self.pk is None
        super().save(*args, **kwargs)

        # We got pk after save above.
        if is_create:
            self.qrcode = str(self.pk)+'.png'
            super().save(update_fields=["qrcode"])

class HistoryData(models.Model):
    """Maim Model with invetory"""
    invent_id = models.IntegerField(default=0, null=True, blank=True)
    username = models.CharField(max_length=60)
    use_date = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):  # new
        return reverse('inventory_details', kwargs={'pk': self.pk})
    def __str__(self):
        return '%s %s %s' % (self.pk, self.username, self.use_date)

@receiver(post_save, sender=InventoryModel)
def signal_handler_history(sender, instance, **kwargs):

    if HistoryData.objects.count() != 0:
        if instance.username != HistoryData.objects.last().username:
            HistoryData.objects.create(username=instance.username, use_date=instance.updated_date, invent_id=instance.pk)
    else:
        HistoryData.objects.create(username=instance.username, use_date=instance.updated_date, invent_id=instance.pk)

@receiver(post_save, sender=InventoryModel)
def signal_handler_qr(sender, instance, **kwargs):
    main_adress = str("http://127.0.0.1/" + str(instance.id) + "/details")
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(main_adress)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    print(str(settings.MEDIA_ROOT)+'/'+ str(instance.pk) + '.png')
    img.save(str(settings.MEDIA_ROOT)+'/'+ str(instance.pk) + '.png')