from django.contrib import admin
from .models import Payee, PayeeAddress, PaymentDetails, Invoice, Appointment

# Register your models here.

admin.site.register(Payee)
admin.site.register(PayeeAddress)
admin.site.register(PaymentDetails)
admin.site.register(Invoice)
admin.site.register(Appointment)