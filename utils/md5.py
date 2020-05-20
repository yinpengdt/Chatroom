#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import qrcode
from io import BytesIO
import base64


def get_sign(params):
    src_md5 = ''
    for key in sorted(params.keys()):
        src_md5 += (key + '=' + str(params[key]) + '&')
    src_md5 = src_md5[:-1]
    return hashlib.md5(src_md5.encode()).hexdigest()


def gen_base64_qrcode(text):
    img = qrcode.make(text)
    buf = BytesIO()
    img.save(buf, format='PNG')
    image_stream = buf.getvalue()
    heximage = base64.b64encode(image_stream)
    return heximage
