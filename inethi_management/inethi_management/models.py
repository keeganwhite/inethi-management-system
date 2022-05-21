from django.db import models


class Payments(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    payment = models.OneToOneField(Payments, on_delete=models.CASCADE, primary_key=True)
    payment_method = models.IntegerField()
    payment_identifier = models.CharField(max_length=10)
    amount = models.FloatField()
    paydate_time = models.DateTimeField()
    service_period_sec = models.IntegerField()
    package = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_identifier
