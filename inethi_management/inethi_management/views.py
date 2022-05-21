from django.http import JsonResponse
from .models import Payment
from .serializers import PaymentSerializer, PaymentsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def payment(request, format=None):
    """
    Get all the payments, serialise them and return json
    :param request: api request body
    :return: json object of all management
    """
    if request.method == 'GET':
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def payment_detail(request, id, format=None):
    try:
        p = Payment.objects.get(pk=id)
    except Payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PaymentSerializer(p)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PaymentSerializer(p, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        p.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
