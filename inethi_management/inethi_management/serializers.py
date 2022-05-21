from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            'id',
            'payment_method',
            'payment_identifier',
            'amount',
            'paydate_time',
            'service_period_sec',
            'package'
        ]


