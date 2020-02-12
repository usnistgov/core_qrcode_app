""" Views for the RandR terms REST API
"""
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import pyqrcode
import io
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import os
import base64
from pathlib import Path

class QRCodeGenCode(APIView):
    """ Generate a new code.
    """

    @csrf_exempt
    def get(self, request):
        """ Get a QR Code.

        Url Parameters:

            record: record

        Examples:

            ../gen-code/?record=[record]

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: QR Code PNG
        """
        try:
            # Generate a QR Code.
            record = request.GET['record']
            record = self.request.query_params.get('record', None)
            if record:
                record = record

            code = pyqrcode.create(record)
            buffer = io.BytesIO()
            code.png(buffer, scale=3)

            return HttpResponse(buffer.getvalue(), content_type="image/png")
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QRCodeEncode(APIView):
    """ Generate a new code with bottom data.
    """

    @csrf_exempt
    def get(self, request):
        """ Get a QR Code with Details.

        Url Parameters:

            record: record

        Examples:

            ../encode/?record=[record]

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: QR Code PNG
        """
        try:
            # Generate a QR Code.
            record = request.GET['record']

            qr_code = "http://127.0.0.1:8000/core_qrcode_app/gen_code?record={0}".format(record)
            details = "Fe0-1 Arc-melted Homogenized 1250 C; 48 h;FC Annealed 800 C, 168h, WQ Lass 10-9-18"
            body = '<html><head></head><body><div><img src="{0}"/><strong style="text-align: center;"><p style="text-align: left; margin-left: 1%; width: 160px;">{1}</p></strong></div></body></html>'.format(qr_code, details)
            return HttpResponse(body, content_type="text/html")#, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QRCodeGetCode(APIView):
    """ Recognize a QR Code.
    """

    @csrf_exempt
    def post(self, request):
        """ Detect the url encoded in the QR Code.

        Examples:

            ../get-code

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: Url
        """
        try:
            # Generate a QR Code.
            buffer = io.BytesIO()
            buffer.write(request.FILES['file'].read())

            buffer.seek(0)
            buffer_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)

            im = cv2.imdecode(buffer_bytes, cv2.IMREAD_COLOR)
            decodedObjects = pyzbar.decode(im)
            for obj in decodedObjects:
                return Response(obj.data.decode(), content_type="text/text", status=status.HTTP_200_OK)

            return Response("Error: Could not decode the QR Code.", content_type="text/text", status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QRCodeDecode(APIView):
    """ Recognize a QR Code from a Camera.
    """

    @csrf_exempt
    def get(self, request):
        """ Detect the url encoded from a Camera capture.

        Examples:

            ../decode

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: Url
        """
        try:
            # Generate a QR Code.
            return HttpResponse(open("{0}/static/core_qrcode_app/user/html/capture.html".format(Path(os.path.dirname(os.path.realpath(__file__))).parent), "r").read(), content_type="text/html")
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
