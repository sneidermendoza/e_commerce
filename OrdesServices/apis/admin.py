from django.contrib import admin
from .models import Orders,OrderDetails
# Register your models here.
admin.site.register(Orders)
admin.site.register(OrderDetails)