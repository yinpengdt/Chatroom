#!/usr/bin/env python
# -*- coding: utf-8 -*-

REDIS = {
    'vadd0': {'address': '10.10.55.146', 'db': 0},
}

A_HOUR = 3600
HOUR6 = 6 * A_HOUR
HOUR3 = 3 * A_HOUR
A_DAY = 24 * A_HOUR

try:
    from tornado.options import options
    import logging
    if options.debug:
        exec(compile(open('settings_debug.py').read(), 'settings_debug.py', 'exec'))
except Exception as e:
    logging.error(e)
    exec(compile(open('settings_debug.py').read(), 'settings_debug.py', 'exec'))