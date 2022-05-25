import json
from _datetime import datetime
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
            dic = json.load(request)
            service_type = dic['service_type_id']
            if 'phone_num' in dic:
                phone_num = dic['phone_num']
                try:
                    user = Users.objects.get(phonenum_encrypt=phone_num)
                    user_id = user.id
                    limit = UserPaymentLimits.objects.get(user_id=user_id, service_type_id=service_type)
                    serializer = UserPaymentLimitsSerializer(limit)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Users.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif 'email' in dic:
                email = dic['email']
                try:
                    user = Users.objects.get(email_encrypt=email)
                    user_id = user.id
                    limit = UserPaymentLimits.objects.get(user_id=user_id, service_type_id=service_type)
                    serializer = UserPaymentLimitsSerializer(limit)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Users.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif 'email' in dic:
                keycloak_id = dic['keycloak_id']
                try:
                    user = Users.objects.get(keycloak_id=keycloak_id)
                    user_id = user.id
                    limit = UserPaymentLimits.objects.get(user_id=user_id, service_type_id=service_type)
                    serializer = UserPaymentLimitsSerializer(limit)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Users.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        except UserPaymentLimits.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def check_payment_default_limit(request, format=None):
    if request.method == 'GET':
        try:
            service_type = request.data['service_type']
            payment_method = request.data['payment_method']
            try:
                limit = DefaultPaymentLimits.objects.get(service_type=service_type, payment_method=payment_method)
                serializer = DefaultPaymentLimitsSerializer(limit)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except DefaultPaymentLimits.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def purchase(request, format=None):
    if request.method == 'POST':
        try:
            dic = json.load(request)
            payment_method = dic['payment_method']
            amount = dic['amount']
            service_period_sec = dic['service_period_sec']
            package = dic['package']
            service_type = dic['service_type_id']
            if 'phone_num' in dic:
                phone_num = dic['phone_num']
                try:
                    user = Users.objects.get(phonenum_encrypt=phone_num)
                except Users.DoesNotExist:
                    user = Users.objects.create(phonenum_encrypt=phone_num, joindate_time=datetime.now())
            elif 'email' in dic:
                email = dic['email']
                try:
                    user = Users.objects.get(email_encrypt=email)
                except Users.DoesNotExist:
                    user = Users.objects.create(email_encrypt=email, email=datetime.now())
            elif 'keycloak_id' in dic:
                keycloak_id = dic['keycloak_id']
                try:
                    user = Users.objects.get(keycloak_id=keycloak_id)
                except Users.DoesNotExist:
                    user = Users.objects.create(keycloak_id=keycloak_id, joindate_time=datetime.now())
            try:
                limit = DefaultPaymentLimits.objects.get(service_type=service_type, payment_method=payment_method)
            except DefaultPaymentLimits.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                limit = UserPaymentLimits.objects.get(user_id=user.id, service_type_id=service_type)
            except UserPaymentLimits.DoesNotExist:
                pass
            payment = Payment.objects.create(user_id=user, payment_method=payment_method,
                                             amount=amount,
                                             paydate_time=datetime.now(), service_period_sec=service_period_sec,
                                             package=package)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def request_user_data(request, format=None):
    if request.method == 'GET':
        try:
            keycloak_id = request.data['keycloak_id']
            try:
                user = Users.objects.get(keycloak_id=keycloak_id)
                serializer = UsersSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except DefaultPaymentLimits.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)