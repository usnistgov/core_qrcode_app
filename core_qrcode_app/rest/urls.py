"""Url router for the REST API
"""
from django.urls import re_path

from core_qrcode_app.rest.qr_utils import views as qrcode_views

urlpatterns = [
    re_path(r'^gen-code/$',
        qrcode_views.QRCodeGenCode.as_view(),
        name='core_qrcode_app_rest_gen_code'),

    re_path(r'^encode/$',
        qrcode_views.QRCodeEncode.as_view(),
        name='core_qrcode_app_rest_encode'),

    re_path(r'^get_code/$',
        qrcode_views.QRCodeGetCode.as_view(),
        name='core_qrcode_app_rest_get_code'),

    re_path(r'^encode/$',
        qrcode_views.QRCodeDecode.as_view(),
        name='core_qrcode_app_rest_decode'),
]
