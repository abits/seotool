# -*- coding: utf8 -*-
import os
from oauth2client.client import flow_from_clientsecrets
BASEDIR = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'DrZy8)3*h#c(-k$a;Sy6YY<ÜT,=i$tLk]9üU_Rh>xb[fNJDcCjNfHucF.]Ä,yfQ,'

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_NAME = 'test'

# Declare constants and set configuration values
# The file with the OAuth 2.0 Client details for authentication and
# authorization.
CLIENT_SECRETS = os.path.join(BASEDIR, 'client_secrets.json')

# A helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = '%s is missing' % CLIENT_SECRETS

# The Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
                               scope=['https://www.googleapis.com/auth/analytics.readonly',
                                      'https://www.googleapis.com/auth/analytics'],
                               redirect_uri='http://seotool.codeways.org/authorized',
                               message=MISSING_CLIENT_SECRETS_MESSAGE)