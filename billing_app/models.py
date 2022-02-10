from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

APPOINTMENT_TYPES = (
    (1, "Appointment"),
    (2, "Late Cancellation"),
    (3, "No-Show")
)

class Payee(models.Model):
    '''Invoice recipients'''
    payee_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.payee_name

class PayeeAddress(models.Model):
    '''Invoice recipient addresses'''
    payee_name = models.ForeignKey(Payee, on_delete=models.CASCADE)
    payee_address_line_1 = models.CharField(max_length=50)
    payee_address_line_2 = models.CharField(max_length=50)
    payee_address_city = models.CharField(max_length=20)
    payee_address_county = models.CharField(max_length=25)
    payee_address_eircode = models.CharField(max_length=7)

    class Meta:
        ordering = ['-payee_name']

    def __str__(self):
        return self.title

class PaymentDetails(models.Model):
    '''Remittance Details'''
    payment_number = models.PositiveSmallIntegerField(unique=True)
    payment_date = models.DateField()
    payment_amount = models.DecimalField(decimal_places=2, max_digits=6)
    payment_method = models.CharField(max_length=15)
    payment_is_cleared = models.BooleanField()

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return self.payment_number

class Invoice(models.Model):
    '''Invoices'''
    invoice_number = models.PositiveSmallIntegerField(unique=True)
    payee_name = models.ForeignKey(Payee, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    invoice_sent_date = models.DateField()
    payment_number = models.ForeignKey(
        PaymentDetails, blank=True, default='', on_delete=models.SET_DEFAULT
    )
    payment_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-invoice_number']

    def __str__(self):
        return self.invoice_number

class Appointment(models.Model):
    '''Appointment Details'''
    invoice_number = models.ForeignKey(
        Invoice, null=True, default='', on_delete=models.SET_DEFAULT
    )
    appointment_datetime = models.DateTimeField()
    appointment_type = models.PositiveSmallIntegerField(
        choices=APPOINTMENT_TYPES, default=1, blank=False
    )
    appointment_fee = models.DecimalField(
        decimal_places=2, max_digits=3, blank=False
    )

    class Meta:
        ordering = ['-appointment_datetime']

    def __str__(self):
        return self.appointment_type
