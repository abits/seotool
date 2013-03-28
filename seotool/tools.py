# -*- coding: utf-8 -*-
# Tools module.
# This module contains static helper functions.  They should receive all dependencies as parameters.

from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import *
from reportlab.lib.styles import getSampleStyleSheet


def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)

    return validate


def render_line_chart(data):

    drawing = Drawing(600, 250)
    lc = HorizontalLineChart()
    lc.x = 50
    lc.y = 50
    lc.height = 250
    lc.width = 600
    lc.data = data
    lc.joinedLines = 1
    lc.categoryAxis.labels.boxAnchor = 'n'
    lc.valueAxis.valueMin = 0
    lc.valueAxis.valueMax = 2000
    lc.valueAxis.valueStep = 500
    lc.lines[0].strokeWidth = 6
    lc.lines[1].strokeWidth = 4.5
    drawing.add(lc)

    drawing.save(formats=['png', 'svg'], outDir='seotool/static/img', fnRoot='example')
    return 'img/example.svg'
