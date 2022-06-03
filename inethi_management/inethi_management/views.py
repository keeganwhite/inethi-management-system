import json
from _datetime import datetime
from datetime import timedelta

from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pytz


@api_view(['GET'])
def check_payment_user_limit(request, format=None):
    if request.method == 'GET':
        try:
            dic = json.load(request)
            service_type = dic['service_type_id']
            payment_method = dic["payment_method"]
            if 'phone_num' in dic:
                phone_num = dic['phone_num']
                try:
                    user = Users.objects.get(phonenum_encrypt=phone_num)
                    limit = UserPaymentLimits.objects.get(user_id=user, service_type_id=service_type,
                                                          payment_method=payment_method)

                    serializer = UserPaymentLimitsSerializer(limit)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Users.DoesNotExist:
                    return JsonResponse(status=404, data={'error': 'user not registered'})
                except UserPaymentLimits.DoesNotExist:
                    return JsonResponse(status=404, data={'error': 'user payment limit not set'})
            elif 'email' in dic:
                email = dic['email']
                try:
                    user = Users.objects.get(email_encrypt=email)
                    limit = UserPaymentLimits.objects.get(user_id=user, service_type_id=service_type,
                                                          payment_method=payment_method)
                    serializer = UserPaymentLimitsSerializer(limit)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Users.DoesNotExist:
                    return JsonResponse(status=404, data={'error': 'user not registered'})
                except UserPaymentLimits.DoesNotExist:
                    return JsonResponse(status=404, data={'error': 'user payment limit not set'})
            elif 'keycloak_id' in dic:
                keycloak_id = dic['keycloak_id']
                try:
                    user = Users.objects.get(keycloak_id=keycloak_id)
                    limit = UserPaymentLimits.objects.get(user_id=user, service_type_id=service_type,
                                                          payment_method=payment_method)
                    serializer = UserPaymentLimitsSerializer(limit)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Users.DoesNotExist:
                    return JsonResponse(status=404, data={'error': 'user not registered'})
                except UserPaymentLimits.DoesNotExist:
                    return JsonResponse(status=404, data={'error': 'user payment limit not set'})
        except:
            return JsonResponse(status=400, data={'error': 'incorrectly formatted request'})


@api_view(['GET'])
def check_payment_default_limit(request, format=None):
    if request.method == 'GET':
        try:
            service_type = request.data['service_type']
            payment_method = request.data['payment_method']
            try:
                limit = DefaultPaymentLimits.objects.get(service_type_id=service_type, payment_method=payment_method)
                serializer = DefaultPaymentLimitsSerializer(limit)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except DefaultPaymentLimits.DoesNotExist:
                return JsonResponse(status=404, data={'error': 'default payment limit not set'})
        except:
            return JsonResponse(status=400, data={'error': 'incorrectly formatted request'})


@api_view(['POST'])
def purchase(request, format=None):
    """
    End point to register a purchase. User is registered if not already registered, payment method is checked, payment
    limit is checked and a payment is added to the DB if all these requirements are met.
    :param request: JSON object
    :param format: optional requirement to change browser format
    :return: http status and message
    """
    if request.method == 'POST':
        try:
            dic = json.load(request)
            payment_method = dic['payment_method']  # int indicating payment method (type)
            amount = dic['amount']
            service_period_sec = dic['service_period_sec']
            package = dic['package']  # description of service
            service_type = dic['service_type_id']  # registered service IDs
            if 'phone_num' in dic:
                phone_num = dic['phone_num']
                try:
                    user = Users.objects.get(phonenum_encrypt=phone_num)
                except Users.DoesNotExist:
                    user = Users.objects.create(phonenum_encrypt=phone_num, joindate_time=datetime.now())  # create
                    # user if they do not exist in the DB
            elif 'email' in dic:
                email = dic['email']
                try:
                    user = Users.objects.get(email_encrypt=email)
                except Users.DoesNotExist:
                    user = Users.objects.create(email_encrypt=email, email=datetime.now())  # create
                    # user if they do not exist in the DB
            elif 'keycloak_id' in dic:
                keycloak_id = dic['keycloak_id']
                try:
                    user = Users.objects.get(keycloak_id=keycloak_id)
                except Users.DoesNotExist:
                    user = Users.objects.create(keycloak_id=keycloak_id, joindate_time=datetime.now())  # create
                    # user if they do not exist in the DB
            else:
                return JsonResponse(status=400, data={'error': 'no user identifier found'})
            try:
                limit = DefaultPaymentLimits.objects.get(service_type_id=service_type, payment_method=payment_method)
            except DefaultPaymentLimits.DoesNotExist:
                return JsonResponse(status=404, data={'error': 'default payment limit not set'})
            limit_user_exists = False
            try:
                limit_user = UserPaymentLimits.objects.get(user_id=user, service_type_id=service_type,
                                                           payment_method=payment_method)
                limit_user_exists = True
            except UserPaymentLimits.DoesNotExist:
                pass  # this doesn't matter as limit would have been set above by default
            if limit_user_exists:
                limit = limit_user
            total_spent = 0

            try:
                last_payment = Payment.objects.filter(user_id=user, service_type_id=service_type,
                                                      payment_method=payment_method).latest('paydate_time')
            except Payment.DoesNotExist:
                last_payment = None
            print("The payment limit is", limit.payment_limit)
            if last_payment is not None:
                print("Found last payment")
                try:
                    start = datetime.now() - timedelta(seconds=limit.payment_limit_period_sec)
                    latest_payments = Payment.objects.filter(
                        paydate_time__range=[start, datetime.now(tz=pytz.utc)]).values_list('amount', flat=True)
                    latest_payments = list(latest_payments)
                    for payments in latest_payments:
                        total_spent = total_spent + payments
                except Exception as e:
                    print(e)
                    return JsonResponse(status=404, data={'error': 'cannot retrieve payments'})
            total_spent = total_spent + amount
            print("total spent", total_spent)
            if last_payment is not None:
                last_payment_time = last_payment.paydate_time
                time_now = datetime.now()
                naive_payment_time = last_payment_time.replace(tzinfo=None)
                naive_time_now = time_now.replace(tzinfo=None)
                delta = naive_time_now - naive_payment_time  # fixes naive vs aware time
                if delta.seconds > limit.payment_limit_period_sec or total_spent <= limit.payment_limit:
                    try:
                        payment = Payment.objects.create(user_id=user, payment_method=payment_method, amount=amount,
                                                         paydate_time=datetime.now(tz=pytz.UTC),
                                                         service_type_id=service_type,
                                                         service_period_sec=service_period_sec,
                                                         package=package)
                    except Exception as e:
                        print(e)
                    serializer = PaymentSerializer(payment)
                    print("first if (last payment exists)")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                elif total_spent >= limit.payment_limit:
                    print("second elif (last payment exists)")
                    return JsonResponse(status=400, data={'error': 'payment limit exceeded in time window'})  # TODO add time remaining
                elif delta.seconds < limit.payment_limit_period_sec:  # TODO test removing this
                    print("first elif (last payment exists)")
                    return JsonResponse(status=400, data={'error': 'time limit exceeded'})
            elif limit.payment_limit >= total_spent:
                print("first elif (last payment does not exist)")
                print(amount)
                payment = Payment.objects.create(user_id=user, payment_method=payment_method,
                                                 amount=amount,
                                                 paydate_time=datetime.now(tz=pytz.UTC),
                                                 service_period_sec=service_period_sec,
                                                 service_type_id=service_type, package=package)
                serializer = PaymentSerializer(payment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return JsonResponse(status=400, data={'error': 'payment limit exceeded'})  # TODO add payment limit

        except Exception as e:
            print(e)
            return JsonResponse(status=400, data={'error': 'incorrectly formatted request'})


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


@api_view(['POST'])
def register_user(request, format=None):
    if request.method == 'POST':
        dic = json.load(request)
        print(dic)
        if 'phone_num' in dic:
            phone_num = dic['phone_num']
            user = Users.objects.create(phonenum_encrypt=phone_num, joindate_time=datetime.now(tz=pytz.UTC))
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif 'email' in dic:
            email = dic['email']
            user = Users.objects.create(email_encrypt=email, email=datetime.now(tz=pytz.UTC))
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif 'keycloak_id' in dic:
            keycloak_id = dic['keycloak_id']
            user = Users.objects.create(keycloak_id=keycloak_id, joindate_time=datetime.now(tz=pytz.UTC))
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(status=400, data={'error': 'no user identifier found'})


@api_view(['GET'])
def request_services(request, format=None):
    if request.method == 'GET':
        services = ServiceTypes.objects.all()
        serializer = ServiceTypesSerializer(services, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_latest_purchase(request, format=None):
    if request.method == 'GET':
        dic = json.load(request)
        service_type_id = dic['service_type_id']
        phone_num = dic['phone_num']
        user = Users.objects.get(phonenum_encrypt=phone_num)
        payment_method = dic['payment_method']
        try:
            latest_payment = Payment.objects.filter(user_id=user, service_type_id=service_type_id,
                                                    payment_method=payment_method).latest('paydate_time')
            serializer = PaymentSerializer(latest_payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return JsonResponse(status=404, data={'error': 'no payments found'})


@api_view(['GET'])
def get_time_since_last_purchase(request, format=None):
    if request.method == 'GET':
        dic = json.load(request)
        service_type_id = dic['service_type_id']
        phone_num = dic['phone_num']
        user = Users.objects.get(phonenum_encrypt=phone_num)
        payment_method = dic['payment_method']
        try:
            latest_payment = Payment.objects.filter(user_id=user, service_type_id=service_type_id,
                                                    payment_method=payment_method).latest('paydate_time')
        except Payment.DoesNotExist:
            return JsonResponse(status=404, data={'error': 'no payments found'})
        except Users.DoesNotExist:
            return JsonResponse(status=404, data={'error': 'no user found'})
        last_payment_time = latest_payment.paydate_time
        time_now = datetime.now()
        naive_payment_time = last_payment_time.replace(tzinfo=None)
        naive_time_now = time_now.replace(tzinfo=None)
        delta = naive_time_now - naive_payment_time  # fixes naive vs aware time
        return JsonResponse(status=200, data={'time_difference': delta.seconds})


@api_view(['GET'])
def get_last_payments_by_time_period(request, format=None):
    if request.method == 'GET':
        try:
            dic = json.load(request)
            payment_limit_period_sec = dic["payment_limit_period_sec"]
            start = datetime.now() - timedelta(seconds=payment_limit_period_sec)
            latest_payments = Payment.objects.filter(
                paydate_time__range=[start, datetime.now(tz=pytz.utc)]).values_list('amount', flat=True)
            latest_payments = list(latest_payments)
            print(latest_payments)
            return JsonResponse(status=200, data=latest_payments, safe=False)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
