from django.db import models


class ServiceTypes(models.Model):
    description = models.CharField(max_length=100)
    pay_type = models.IntegerField()
    payment_methods_supported = models.IntegerField()  # what is this?

    def __str__(self):
        return str(self.description)


class Payments(models.Model):
    service_type = models.ForeignKey(ServiceTypes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.service_type)


class Payment(models.Model):
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE)
    payment_method = models.IntegerField()
    payment_identifier = models.CharField(max_length=10)
    amount = models.FloatField()
    paydate_time = models.DateTimeField()
    service_period_sec = models.IntegerField()
    package = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_identifier


class Users(models.Model):
    keycloak_id = models.CharField(max_length=100, unique=True)
    services = models.IntegerField()
    email_encrypt = models.CharField(max_length=100)
    phonenum_encrypt = models.CharField(max_length=100)
    # payment_users_limits_id = models.IntegerField()
    joindate_time = models.DateTimeField()

    def __str__(self):
        return str(self.keycloak_id)


class UserPaymentLimits(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    service_type_id = models.ForeignKey(ServiceTypes, on_delete=models.CASCADE)
    payment_method = models.IntegerField()
    payment_limit = models.IntegerField()
    payment_limit_period_days = models.IntegerField()

    def __str__(self):
        return str(self.user_id)


class Service(models.Model):
    service_type_id = models.ForeignKey(ServiceTypes, on_delete=models.DO_NOTHING)
    payments_id = models.ForeignKey(Payments, on_delete=models.DO_NOTHING)
    user_encrypt = models.CharField(max_length=100)
    pass_encrypt = models.CharField(max_length=100)
    join_datetime = models.DateTimeField()
    misc1 = models.CharField(max_length=100)
    misc2 = models.CharField(max_length=100)

    def __str__(self):
        return str(self.service_type_id)


class Services(models.Model):
    service_id = models.OneToOneField(Service, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.service_id)


class DefaultPaymentLimits(models.Model):
    service_type = models.OneToOneField(ServiceTypes, on_delete=models.CASCADE)
    payment_method = models.IntegerField()
    payment_limit = models.IntegerField()
    payment_limit_period_sec = models.IntegerField()

    def __str__(self):
        return str(self.service_type)
