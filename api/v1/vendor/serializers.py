from rest_framework import serializers
from home.models import *
from django.utils import timezone

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_id', 'name', 'vendor_code', 'contact_details', 'address']
    
    def update(self, instance, validated_data):
        if not validated_data or validated_data == {}:
            raise serializers.ValidationError('No data has been Provided!')
        return super().update(instance, validated_data)


class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = serializers.CharField()

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
    
    def validate_vendor(self, value):
        try:
            vendor = Vendor.objects.get(vendor_code=value)
            return vendor
        except:
            raise serializers.ValidationError('Invalid Vendor Code!')
    

class UpdatePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['status', 'quality_rating', 'issue_date']
    
    def validate(self, attrs):
        if 'status' in attrs and attrs['status'] == 'completed' and 'quality_rating' not in attrs:
            raise serializers.ValidationError('Quality Rating should be provided while updating Status')
        return attrs
    
    def update(self, instance, validated_data):
        if not validated_data or validated_data == {}:
            print(validated_data)
            raise serializers.ValidationError('No data has been Provided!')
        return super().update(instance, validated_data)


class AcknowledgePurchaseOrderSerializer(serializers.Serializer):
    acknowledgment_date = serializers.DateTimeField(required=False)
    
    def update(self, instance, validated_data):
        acknowledgment_date = validated_data.get('acknowledgment_date')

        if acknowledgment_date is None:
            acknowledgment_date = timezone.localtime(timezone.now())
        instance.acknowledgment_date = acknowledgment_date
        instance.save()
        return instance


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['contact_details', 'address']


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'