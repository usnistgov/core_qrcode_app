core_qrcode_app
===========================

QR Code for core project.

Quick start
===========

1. Add "core_qrcode_app" to your INSTALLED_APPS setting
-------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_qrcode_app', # /!\ Should always be placed before core_explore_keyword_app
      'core_explore_keyword_app',
    ]
