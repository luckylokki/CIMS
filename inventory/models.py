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

    class Meta:
        ordering = ['op_system']

    def __str__(self) -> str:
        return self.op_system


class FactoryModel(models.Model):
    """Model for Factory names"""
    factory_name = models.CharField(max_length=30, blank=False)

    class Meta:
        ordering = ['factory_name']

    def __str__(self) -> str:
        return self.factory_name


class MainDomain(models.Model):
    """Model for Factory names"""
    domain_name = models.CharField(max_length=40, blank=False)

    def __str__(self) -> str:
        return self.domain_name


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
    second_serial_number = models.CharField(max_length=30, blank=True)
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
    updated_by = CurrentUserField(on_update=True, related_name='updated_by')
    price_buy = models.IntegerField(default=0, null=True, blank=True)
    price_today = models.IntegerField(default=0, null=True, blank=True)
    price_sell = models.IntegerField(default=0, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
    new_purchase = models.BooleanField(default=False)

    def get_absolute_url(self):  # new
        return reverse('inventory_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        is_create = self.pk is None
        super().save(*args, **kwargs)

        # We got pk after save above.
        if is_create:
            self.qrcode = 'qr/' + str(self.pk) + '.png'
            super().save(update_fields=["qrcode"])


class PurchaseData(models.Model):
    """History model who used inventory before"""
    link_id = models.IntegerField(default=0, null=True, blank=True)
    username = models.CharField(max_length=60)
    model_fact = models.CharField(max_length=60)
    type_name = models.CharField(max_length=30, null=True)
    buy_date = models.DateTimeField(auto_now_add=True, null=True)
    price_buy = models.IntegerField(default=0, null=True, blank=True)
    serial_number = models.CharField(max_length=30, blank=True)

    def get_absolute_url(self):  # new
        return reverse('inventory_purchase', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s %s %s %s %s %s' % (
            self.pk, self.model_fact, self.username, self.buy_date, self.price_buy, self.serial_number)


class HistoryData(models.Model):
    """Maim Model with invetory"""
    invent_id = models.IntegerField(default=0, null=True, blank=True)
    username = models.CharField(max_length=60)
    sys_user = models.CharField(max_length=60)  # system suer who do record
    use_date = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):  # new
        return reverse('inventory_details', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s %s %s %s' % (self.pk, self.username, self.use_date, self.sys_user)


@receiver(post_save, sender=InventoryModel)
def signal_handler_history(sender, instance, **kwargs):
    print(get_default_datetime())
    if HistoryData.objects.count() != 0:
        if HistoryData.objects.filter(invent_id=instance.pk).exists():
            if instance.username != HistoryData.objects.filter(invent_id=instance.pk).last().username:
                HistoryData.objects.create(username=instance.username, use_date=instance.updated_date,
                                           invent_id=instance.pk, sys_user=instance.updated_by)
        else:
            HistoryData.objects.create(username=instance.username, use_date=instance.updated_date,
                                       invent_id=instance.pk,
                                       sys_user=instance.updated_by)
    else:
        HistoryData.objects.create(username=instance.username, use_date=instance.updated_date, invent_id=instance.pk,
                                   sys_user=instance.updated_by)


@receiver(post_save, sender=InventoryModel)
def signal_handler_purchase(sender, instance, **kwargs):
    fm = str(instance.factory_name) + ' ' + str(instance.model_name)
    if instance.new_purchase == 1:
        if not PurchaseData.objects.filter(link_id=instance.pk).exists():
            PurchaseData.objects.create(link_id=instance.pk, username=instance.username,
                                        model_fact=fm,type_name=instance.type_name,
                                        buy_date=instance.created_date, price_buy=instance.price_buy,
                                        serial_number=instance.serial_number)


@receiver(post_save, sender=InventoryModel)
def signal_handler_qr(sender, instance, **kwargs):
    main_adress = str(str(MainDomain.objects.all()[:1].get()) + 'inventory/' + str(instance.id) + "/details")
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(main_adress)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(str(settings.STATIC_FOLDER) + '/qr/' + str(instance.pk) + '.png')
