from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('vendor/', VendorView.as_view(), name='vendor_view'),
    re_path(r'^vendor/(?P<vendor_id>\d+|[a-zA-Z]+)/$', SpecificVendorView.as_view(), name='specific_vendor_view'),
    re_path(r'^vendor/(?P<vendor_id>\d+|[a-zA-Z]+)/performance/$', VendorPerformanceView.as_view(), name='vendor_performance'),
    path('purchase_orders/', PurchaseOrderView.as_view(), name='purchase_orders'),
    path('purchase_orders/<int:po_id>/', SpecificPurchaseOrderView.as_view(), name='specific_purchase_order'),
    path('purchase_orders/<int:po_id>/acknowledge', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
]
