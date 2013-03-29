# -*- coding: utf-8 -*-
# Services module.
# This module contains Manager classes which handle the primary business logic of the application.
# Managers typically but not necessarily use models and providers to query data.  They are instantiated
# in the view layer.
from seotool import app, db, tools, providers
from datetime import datetime, date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import *


class ChartManager(object):
    """
    Provide chart images and flowable drawing objects for reportlab.
    """
    def get_chart(self, data):
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
        return drawing

    def render_line_chart(self, data):
        drawing = self.get_chart(data)
        drawing.save(formats=['png', 'svg'], outDir='seotool/static/img', fnRoot='example')
        return 'img/example.svg'


class ReportManager(object):
    """
    Generate, archive and retrieve a report.
    """

    def __init__(self):
        self.reports = db.reports

    def create_report(self, profile_id, user):
        report = self.reports.Report()
        report.profile_id = profile_id
        report.created_at = datetime.utcnow()
        report.modified_at = datetime.utcnow()
        report.deleted_at = None
        report.last_author = user._get_current_object()
        report.save()
        return report._id

    def update_configuration(self, report_id, configuration_data):
        report = self.reports.Report.one({'_id': report_id})
        report.configuration = configuration_data
        report.save()

    def save_pdf(self, report_id):
        report = self.reports.Report.one({'_id': report_id})
        pdf = PdfManager()
        pdf.save(report)
        print report


class PdfManager(object):
    title = "Hello world"
    pageinfo = "platypus example"
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()

    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 108, self.title)
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "First Page / %s" % self.pageinfo)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()

    def save(self, report):
        print "Writing shit."
        doc = SimpleDocTemplate("phello.pdf")
        Story = [Spacer(1, 2 * inch)]
        style = self.styles["Normal"]
        for i in range(10):
            bogustext = ("This is Paragraph number %s. " % report._id) * 20
            p = Paragraph(bogustext, style)
            Story.append(p)
            Story.append(Spacer(1, 0.2 * inch))
        al = providers.Analytics()
        profile_id = al.get_profile_id(report.profile_id)
        parameters = {
            'ids': profile_id,
            'start_date': date(2009, 3, 3),
            'end_date': date(2010, 3, 3),
            'metrics': 'visits',
            'dimensions': 'month'
        }
        data = al.retrieveData(parameters)
        cm = ChartManager()
        chart = cm.get_chart(data)
        Story.append(chart)
        for i in range(10):
            bogustext = ("This is Paragraph number %s. " % report._id) * 20
            p = Paragraph(bogustext, style)
            Story.append(p)
            Story.append(Spacer(1, 0.2 * inch))
        doc.build(Story,
                  onFirstPage=self.myFirstPage,
                  onLaterPages=self.myLaterPages)





