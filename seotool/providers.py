# -*- coding: utf-8 -*-
# Providers module.
# Provider classes handle the communication with remote services to provide external data for the system, e.g.
# calling Google Analytics API and provide table data.  Providers simple _serve_ the data, they do not transform
# the data.  They however extract the data from the api response in an easily consumable format,
# e.g. lists of integers etc.

from flask import g
from apiclient.discovery import build
from oauth2client.client import AccessTokenRefreshError, OAuth2Credentials
from apiclient.errors import HttpError
from httplib2 import Http
import json


class InvalidCredentialsError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Analytics(object):

    _service = None

    def initialize_service(self):
        if not self._service:
            credentials = OAuth2Credentials.from_json(json.dumps(g.user.credentials))
            if credentials is None or credentials.invalid:
                raise InvalidCredentialsError('Invalid credentials')
            http = Http()
            try:
                http = credentials.authorize(http)
                self._service = build('analytics', 'v3', http=http)
            except AccessTokenRefreshError:
                raise InvalidCredentialsError('Invalid token')

    def get_profile_id(self, account_id):
        self.initialize_service()
        profile_id = None
        webproperties = self._service.management().webproperties().list(accountId=account_id).execute()
        if webproperties.get('items'):
            # Get the first Web Property ID
            firstWebpropertyId = webproperties.get('items')[0].get('id')

            # Get a list of all Profiles for the first Web Property of the first Account
            profiles = self._service.management().profiles().list(
                accountId=account_id,
                webPropertyId=firstWebpropertyId).execute()

            if profiles.get('items'):
                # return the first Profile ID
                profile_id = profiles.get('items')[0].get('id')
        return profile_id

    def retrieveData(self, parameters):
        rows = []
        sequence = []
        try:
            self.initialize_service()
        except InvalidCredentialsError:
            pass

        ids = 'ga:' + parameters['ids']
        start_date = parameters['start_date'].isoformat()
        end_date = parameters['end_date'].isoformat()
        dimensions = 'ga:' + parameters['dimensions']
        metrics = 'ga:' + parameters['metrics']

        data = self._service.data().ga().get(ids=ids,
                                             start_date=start_date,
                                             end_date=end_date,
                                             metrics=metrics,
                                             dimensions=dimensions).execute()
        for v in data['rows']:
            sequence.append(int(v[1]))

        data = tuple(sequence)
        rows.append(data)

        return rows



