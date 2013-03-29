# -*- coding: utf-8 -*-
# Tools module.
# This module contains static helper functions.  They should receive all dependencies as parameters.
# You should not need classes in here. If you feel the need, consider adding a service class.


def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)

    return validate



