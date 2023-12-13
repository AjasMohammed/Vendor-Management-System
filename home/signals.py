import datetime
from django.db.models.signals import post_save
from django.db.models import F, Avg, ExpressionWrapper, DurationField
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance


@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate_and_quality_rating(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        vendor = instance.vendor

        puchase_orders = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed'
        )

        total_pos = puchase_orders.count()

        on_time_pos = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            acknowledgment_date__lte=F('delivery_date')
        ).count()

        if total_pos > 0 and on_time_pos > 0:
            # Calculates On Time Delivery Rate
            on_time_delivery_rate = (on_time_pos / total_pos) * 100
            vendor.on_time_delivery_rate = on_time_delivery_rate

        quality_rating_avg = puchase_orders.aggregate(
            Avg('quality_rating', default=0))['quality_rating__avg']  # Calculates Average Quality Rating
        vendor.quality_rating_avg = quality_rating_avg

        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def claculate_avg_response_time(sender, instance, created, **kwargs):
    if not created and instance.acknowledgment_date is not None:
        vendor = instance.vendor

        average_response_time = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            acknowledgment_date__isnull=False
        ).aggregate(
            acknowledgment_date__avg=ExpressionWrapper(Avg(F('acknowledgment_date') - F('issue_date')),
                                                       output_field=DurationField()
                                                       ))['acknowledgment_date__avg']

        vendor.average_response_time = average_response_time.days
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def calculate_fulfillment_rate(sender, instance, created, **kwargs):
    if not created and instance.issue_date is not None:
        vendor = instance.vendor

        total_issued_pos = PurchaseOrder.objects.filter(
            vendor=vendor,
            issue_date__isnull=False
        )
        total_number_of_issued_pos = total_issued_pos.count()
        completed_pos = total_issued_pos.filter(status='completed').count()

        if total_number_of_issued_pos > 0 and completed_pos > 0:
            fulfillment_rate = (
                completed_pos / total_number_of_issued_pos) * 100
            vendor.fulfillment_rate = fulfillment_rate
            vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def save_historical_performance(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed' and instance.acknowledgment_date is not None:
        vendor = instance.vendor
        on_time_delivery_rate = vendor.on_time_delivery_rate
        quality_rating_avg = vendor.quality_rating_avg
        average_response_time = vendor.average_response_time
        fulfillment_rate = vendor.fulfillment_rate

        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=datetime.datetime.now(),
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )
    