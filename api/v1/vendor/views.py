from home.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class VendorView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=VendorSerializer,
        responses={201: VendorSerializer(), 400: "Bad Request"},
        operation_description="Create a new vendor"
    )
    def post(self, request):
        """
        Create a new vendor.

        This endpoint creates a new vendor by accepting a POST request with the vendor data.
        """
        data = request.data
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'message': 'Vendor created sucessfully!',
                'data': serializer.data
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: VendorSerializer(many=True)},
        operation_description="Retrieve all vendors"
    )
    def get(self, request):
        """
        Retrieve all vendors.

        This endpoint fetches all existing vendors.
        """
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecificVendorView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_PATH,
                              description="ID or code of the vendor", type=openapi.TYPE_STRING)
        ],
        responses={200: VendorSerializer(), 400: "Bad Request",
                   404: "Not Found"},
        operation_description="Retrieve a specific vendor by ID or code"
    )
    def get(self, request, vendor_id):
        """
        Retrieve a specific vendor by ID or code.

        This endpoint fetches a specific vendor based on the provided ID or code.
        """
        try:
            if vendor_id.isdigit():
                vendor = Vendor.objects.get(vendor_id=vendor_id)
            else:
                vendor = Vendor.objects.get(vendor_code__iexact=vendor_id)

        except Vendor.DoesNotExist:
            context = {'message': 'Invalid ID!'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            context = {'message': ve.detail}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_PATH,
                              description="ID or code of the vendor", type=openapi.TYPE_STRING)
        ],
        request_body=VendorSerializer,
        responses={202: VendorSerializer(), 400: "Bad Request",
                   404: "Not Found"},
        operation_description="Update a specific vendor by ID or code"
    )
    def put(self, request, vendor_id):
        """
        Update a specific vendor by ID or code.

        This endpoint updates a specific vendor identified by the provided ID or code.
        """
        try:
            if vendor_id.isdigit():
                vendor = Vendor.objects.get(vendor_id=vendor_id)
            else:
                vendor = Vendor.objects.get(vendor_code__iexact=vendor_id)

        except Vendor.DoesNotExist:
            context = {'message': 'Invalid ID!'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            context = {'message': ve.detail}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer = VendorSerializer(
            vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                'message': 'Vendor Info Updated Successfully!',
                'data': serializer.data
            }
            return Response(context, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_PATH,
                              description="ID or code of the vendor", type=openapi.TYPE_STRING)
        ],
        responses={200: "OK", 400: "Bad Request", 404: "Not Found"},
        operation_description="Delete a specific vendor by ID or code"
    )
    def delete(self, request, vendor_id):
        """
        Delete a specific vendor by ID or code.

        This endpoint deletes a specific vendor identified by the provided ID or code.
        """
        context = {}
        try:
            if vendor_id.isdigit():
                vendor = Vendor.objects.get(vendor_id=vendor_id)
            else:
                vendor = Vendor.objects.get(vendor_code__iexact=vendor_id)

        except Vendor.DoesNotExist:
            context = {'message': 'Invalid ID!'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            context = {'message': ve.detail}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        vendor.delete()
        context['message'] = 'Vendor Deleted Successfully!'

        return Response(context, status=status.HTTP_200_OK)


class PurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PurchaseOrderSerializer,
        responses={201: PurchaseOrderSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        """
        Create a new Purchase Order.

        This endpoint creates a new Purchase Order.
        """
        data = request.data

        serializer = PurchaseOrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            context = {
                'message': 'Purchase Order initiated sucessfully!',
                'data': serializer.data
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: PurchaseOrderSerializer(many=True)}
    )
    def get(self, request):
        """
        Retrieve all Purchase Orders.

        This endpoint retrieves all existing Purchase Orders.
        """
        po = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(po, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecificPurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: PurchaseOrderSerializer()}
    )
    def get(self, request, po_id):
        """
        Retrieve a specific Purchase Order by ID.

        This endpoint retrieves a specific Purchase Order by its ID.
        """
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            context = {'message': 'Invalid ID!'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            context = {'message': ve.detail}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UpdatePurchaseOrderSerializer,
        responses={202: "Purchase Order Updated Successfully!",
                   400: "Bad Request"}
    )
    def put(self, request, po_id):
        """
        Update a specific Purchase Order by ID.

        This endpoint updates a specific Purchase Order by its ID.
        """
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
            serializer = UpdatePurchaseOrderSerializer(
                purchase_order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {
                    'message': 'Purchase Order Updated Successfully!',
                    'data': serializer.data
                }
                return Response(context, status=status.HTTP_202_ACCEPTED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PurchaseOrder.DoesNotExist:
            context = {'message': 'Invalid ID!'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            context = {'message': ve.detail}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: "Purchase Order Deleted Successfully!",
                   404: "Invalid ID!"}
    )
    def delete(self, request, po_id):
        """
        Delete a specific Purchase Order by ID.

        This endpoint deletes a specific Purchase Order by its ID.
        """
        context = {}
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
            purchase_order.delete()
            context['message'] = 'Purchase Order Deleted Successfully!'
            return Response(context, status=status.HTTP_200_OK)

        except PurchaseOrder.DoesNotExist:
            context = {'message': 'Invalid ID!'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            context = {'message': ve.detail}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class AcknowledgePurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AcknowledgePurchaseOrderSerializer,
        responses={202: "Purchase Order Acknowledged Successfully!",
                   400: "Bad Request", 404: "Invalid ID!"}
    )
    def post(self, request, po_id):
        """
        Acknowledge a specific Purchase Order.

        This endpoint acknowledges a specific Purchase Order by its ID.
        """
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
            serializer = AcknowledgePurchaseOrderSerializer(
                purchase_order, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                context = {
                    'message': 'Purchase Order Acknowledged Successfully!',
                    'data': serializer.data
                }
                return Response(context, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PurchaseOrder.DoesNotExist:
            context = {'message': 'Invalid ID!'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            context = {'message': ve.detail}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class VendorPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VendorPerformanceSerializer(), 404: "Invalid ID!"}
    )
    def get(self, request, vendor_id):
        """
        Retrieve performance metrics of a specific vendor by ID.

        This endpoint retrieves the performance metrics of a specific vendor identified by their ID.
        """
        try:
            if vendor_id.isdigit():
                vendor = Vendor.objects.get(vendor_id=vendor_id)
            else:
                vendor = Vendor.objects.get(vendor_code__iexact=vendor_id)

        except:
            context = {'message': 'Invalid ID!'}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)
