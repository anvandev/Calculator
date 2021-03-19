from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('calculatoradmin/', admin.site.urls),
    path('', include('calculator.urls')),
]
