from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, parsers
from django.core import serializers


@api_view(['GET'])
def check_payment_user_limit(request, format=None):
    if request.method == 'GET':
        try:
            user = request.data['user_id']
            service_type = request.data['service_type_id']
            limit = UserPaymentLimits.objects.get(user_id=user, service_type_id=service_type)
            serializer = UserPaymentLimitsSerializer(limit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserPaymentLimits.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def check_payment_default_limit(request, format=None):
    if request.method == 'GET':
        try:
            service_type = request.data['service_type_id']
            limit = DefaultPaymentLimits.objects.get(service_type_id=service_type)
            serializer = DefaultPaymentLimits(limit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserPaymentLimits.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)