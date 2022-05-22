from django.db import models


class ServiceTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    pay_type = models.IntegerField()
    payment_methods_supported = models.IntegerField()
    payment_default_limits_id = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Payments(models.Model):
    id = models.IntegerField(primary_key=True)
    service_type = models.ForeignKey(ServiceTypes, on_delete=models.CASCADE)

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


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    keycloak_id = models.CharField(max_length=100)
    services = models.IntegerField()
    email_encrypt = models.CharField(max_length=100)
    phonenum_encrypt = models.CharField(max_length=100)
    payment_users_limits_id = models.IntegerField()
    joindate_time = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class UserPaymentLimits(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    service_type_id = models.ForeignKey(ServiceTypes, on_delete=models.CASCADE)
    payment_method = models.IntegerField()
    payment_limit = models.IntegerField()
    payment_limit_period_days = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Service(models.Model):
    id = models.IntegerField(primary_key=True)
    service_type_id = models.ForeignKey(ServiceTypes, on_delete=models.DO_NOTHING)
    payments_id = models.ForeignKey(Payments, on_delete=models.DO_NOTHING)
    user_encrypt = models.CharField(max_length=100)
    pass_encrypt = models.CharField(max_length=100)
    join_datetime = models.DateTimeField()
    misc1 = models.CharField(max_length=100)
    misc2 = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class Services(models.Model):
    id = models.IntegerField(primary_key=True)
    service_id = models.OneToOneField(Service, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class DefaultPaymentLimits(models.Model):
    service_type = models.OneToOneField(ServiceTypes, on_delete=models.CASCADE)
    payment_method = models.IntegerField()
    payment_limit = models.IntegerField()
    payment_limit_period_sec = models.IntegerField()

    def __str__(self):
        return str(self.service_type)
