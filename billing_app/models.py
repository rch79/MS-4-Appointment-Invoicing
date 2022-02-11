from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.


class Payee(models.Model):
    '''Invoice recipients'''
    payee_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.payee_name)


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
    payment_number = models.PositiveSmallIntegerField(blank=False, null=True)
    payment_date = models.DateField()
    payment_amount = models.DecimalField(decimal_places=2, max_digits=6)
    payment_method = models.CharField(max_length=15)
    payment_is_cleared = models.BooleanField()

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return str(self.payment_number)


class Invoice(models.Model):
    '''Invoices'''
    invoice_number = models.SmallIntegerField(blank=True, null=True)
    payee_name = models.ForeignKey(Payee, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    invoice_sent_date = models.DateField()
    payment_number = models.ForeignKey(
        PaymentDetails, blank=True, null=True, default='', on_delete=models.SET_DEFAULT
    )
    payment_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-invoice_number']

    def __str__(self):
        return f'Invoice #{self.invoice_number}'


class Appointment(models.Model):
    '''Appointment Details'''

    APPOINTMENT_TYPES = (
        ('AP', 'Appointment'),
        ('NS', 'No-Show'),
        ('LC', 'Late Cancellation')
    )

    invoice_number = models.ForeignKey(
        Invoice, blank=True, default='', on_delete=models.SET_DEFAULT, null=True
    )
    appointment_datetime = models.DateTimeField()
    appointment_type = models.CharField(
        max_length=2, choices=APPOINTMENT_TYPES, default='AP', blank=False
    )
    appointment_fee = models.DecimalField(
        decimal_places=2, max_digits=8, blank=False
    )

    class Meta:
        ordering = ['-appointment_datetime']

    def __str__(self):
        for appointments in self.APPOINTMENT_TYPES:
            if self.appointment_type in appointments:
                return f'{self.appointment_datetime: %d %B %Y at %H:%M} - {x[1]}'



