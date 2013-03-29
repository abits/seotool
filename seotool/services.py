# -*- coding: utf-8 -*-
# Services module.
# This module contains Manager classes which handle the primary business logic of the application.
# Managers typically but not necessarily use models and providers to query data.  They are instantiated
# in the view layer.
from seotool import app, db, tools
from datetime import datetime


class ChartManager(object):
    """
    Provide chart images and flowable drawing objects for reportlab.
    """
    def get_chart(self, chart_type):
        pass


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
        print report








