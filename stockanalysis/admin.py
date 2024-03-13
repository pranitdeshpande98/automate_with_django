from django.contrib import admin
from . models import Stock, StockData

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockData)