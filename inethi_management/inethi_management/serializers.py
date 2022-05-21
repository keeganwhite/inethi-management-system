from rest_framework import serializers
from .models import *


class ServiceTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTypes
        fields = [
            'id',
            'description',
            'pay_type',
            'payment_methods_supported',
            'payment_default_limits_id',
        ]


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = [
            'id'
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            'payment',
            'payment_method',
            'payment_identifier',
            'amount',
            'paydate_time',
            'service_period_sec',
            'package'
        ]

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.payment_id = validated_data.get('payment_id', instance.payment_id)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.payment_identifier = validated_data.get('payment_identifier', instance.payment_identifier)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.paydate_time = validated_data.get('paydate_time', instance.paydate_time)
        instance.service_period_sec = validated_data.get('service_period_sec', instance.service_period_sec)
        instance.package = validated_data.get('package', instance.package)
        instance.save()
        return instance


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = [
            'id',
            'keycloak_id',
            'services',
            'email_encrypt',
            'phonenum_encrypt',
            'payment_users_limits_id',
            'joindate_time'
        ]


class UserPaymentLimitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = [
            'id',
            'service_type_id',
            'payments_id',
            'user_encrypt',
            'pass_encrypt',
            'join_datetime',
            'misc1',
            'misc2'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'service_type_id',
            'payments_id',
            'user_encrypt',
            'pass_encrypt',
            'join_datetime',
            'misc1',
            'misc2'
        ]

