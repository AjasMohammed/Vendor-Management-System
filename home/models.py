from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email


class Vendor(models.Model):
    vendor_id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(_("Name"), max_length=50)
    vendor_code = models.CharField(_("Vendor Code"), max_length=10, unique=True)
    contact_details = models.TextField(_("Contact Details"))
    address = models.TextField(_("Address"), blank=True, null=True)
    on_time_delivery_rate = models.FloatField(_("On Time Delivery Rate"), null=True, blank=True, default=0)
    quality_rating_avg = models.FloatField(_("Quality Rating Average"), null=True, blank=True,default=0)
    average_response_time = models.FloatField(_("Average Response Time"), null=True, blank=True)
    fulfillment_rate = models.FloatField(_("Fulfillment Rate"), null=True, blank=True, default=0)


    class Meta:
        ordering = ['vendor_id']


    def __str__(self) -> str:
        return f'{self.name} - {self.vendor_code}'
    

class PurchaseOrder(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    po_number = models.AutoField(unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, verbose_name=_("Vendor"), on_delete=models.CASCADE)
    order_date = models.DateTimeField(_("Order Date"), auto_now_add=True)
    delivery_date = models.DateTimeField(_("Delivery Date"))
    items = models.JSONField(_("Items"))
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(_("Quality Rating"), null=True, blank=True)
    issue_date = models.DateTimeField(_("Issue Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    acknowledgment_date = models.DateTimeField(_("Acknowledgment Date"), auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        ordering = ['-order_date', 'po_number']

    def clean(self):
        if self.delivery_date < self.order_date:
            raise ValidationError('Invalid Delivery Date!')

    def __str__(self) -> str:
        return f"{self.vendor.vendor_code} - PO-{self.po_number}"
    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, verbose_name=_("vendor"), on_delete=models.CASCADE)
    date = models.DateTimeField(_("Date"), auto_now_add=True)
    on_time_delivery_rate = models.FloatField(_("On Time Delivery Rate"))
    quality_rating_avg = models.FloatField(_("Quality Rating Average"))
    average_response_time = models.FloatField(_("Average Response Time"))
    fulfillment_rate = models.FloatField(_("Fulfillment Rate"))

    def __str__(self) -> str:
        return f"{self.vendor.name} - {self.vendor.vendor_id} - {self.pk}"