from .  import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('stocks/',views.stocks,name='stocks'),
    path('stock-autocomplete/', views.StockAutocomplete.as_view(),name="stock_autocomplete"),
]