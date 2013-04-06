# -*- coding: utf-8 -*-
# Services module.
# This module contains Manager classes which handle the primary business logic of the application.
# Managers typically but not necessarily use models and providers to query data.  They are instantiated
# in the view layer.
from seotool import app, db, tools, providers, model
from datetime import datetime, date
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
import os


class ChartManager(object):
    """
    Provide chart images and flowable drawing objects for reportlab.
    """
    def get_drawing(self, **kwargs):
        if kwargs['chart'] == 'line_chart':
            chart = model.LineChart(kwargs['data'])
        else:
            chart = model.LineChart(kwargs['data'])
        return chart.get_drawing()

    def render_chart(self, **kwargs):
        drawing = self.get_drawing(kwargs)
        drawing.build(formats=['png'],
                      outDir='seotool/static/img',
                      fnRoot='example')
        return 'img/example.svg'

    def retrieve_data(self, **kwargs):
        al = providers.Analytics()
        return al.retrieveData(kwargs)

    def get_chart(self, **kwargs):
        data = self.retrieve_data(kwargs)
        drawing = self.get_drawing(chart=kwargs['chart'], data=data)
        return drawing

    def get_drawings(self, report):
        drawings = []
        for chart_config in report.configuration['charts']:
            drawings.append(self.get_chart(chart_config))
        return drawings


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
        return report

    def update_configuration(self, report, configuration_data):
        report.configuration = configuration_data
        report.save()

    def prepare_report(self, pdf_manager):
        chart_manager = ChartManager()

        #
        # ids = 'ga:' + kwargs['profile_id']
        # start_date = kwargs['start_date'].isoformat()
        # end_date = kwargs['end_date'].isoformat()
        # dimensions = 'ga:' + kwargs['dimensions']
        # metrics = 'ga:' + kwargs['metrics']

        chart = chart_manager.get_chart(
            chart='line_chart',
            profile_id=pdf_manager.report.profile_id,
            start_date=
            {'chart': 'line_chart',

             })
        pdf_manager.charts.append(chart)

    def generate_pdf(self, report):
        ## prep charts
        chart_manager = ChartManager()
        drawings = chart_manager.get_drawings(report)
        pdf_manager = PdfManager(report)
        pdf_manager.prepare(report, drawings)
        directory = os.path.join('reports', str(report.profile_id))
        if not os.path.exists(directory):
            os.mkdir(directory)
        timestamp = int(time.time())
        filename = str(timestamp) + '.pdf'
        pdf_file = os.path.join(directory, filename)
        pdf_manager.output(pdf_file)


class PdfManager(object):
    def __init__(self, report):
        self.report = report
        self.title = "Hello World"
        self.pageinfo = "example"
        self.PAGE_HEIGHT = defaultPageSize[1]
        self.PAGE_WIDTH = defaultPageSize[0]
        self.styles = getSampleStyleSheet()
        self.charts = []

    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0,
                                 self.PAGE_HEIGHT - 108, self.title)
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "First Page / %s" % self.pageinfo)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch,
                          0.75 * inch,
                          "Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()

    def prepare(self, report, drawings):
        pass

    def output(self, pdf_file):
        doc = SimpleDocTemplate(pdf_file)
        Story = [Spacer(1, 2 * inch)]
        style = self.styles["Normal"]
        if self.report.configuration['summary'] != '':
            Story.append(self.report.configuration['summary'])
        for chart in self.charts:
            Story.append(chart)


        al = providers.Analytics()
        profile_id = al.get_profile_id(self.report.profile_id)
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


        doc.build(Story,
                  onFirstPage=self.myFirstPage,
                  onLaterPages=self.myLaterPages)





