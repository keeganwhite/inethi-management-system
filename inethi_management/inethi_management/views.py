from django.http import JsonResponse
from .models import Payment
from .serializers import PaymentSerializer


def payment_list(request):
    """
    Get all the payments, serialise them and return json
    :param request: api request body
    :return: json object of all management
    """
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return JsonResponse(serializer.data, safe=False)
