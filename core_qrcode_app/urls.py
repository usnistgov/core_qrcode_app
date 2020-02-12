""" Url router for the qrcode application
"""
from django.conf.urls import include
from django.urls import re_path

urlpatterns = [
    re_path(r'^rest/', include('core_qrcode_app.rest.urls')),
]
