import os
import unittest

import requests

BASE_URL = os.environ.get('BASE_URL') or 'http://pay.dev'
EXAMPLE_URL = BASE_URL
UI_URL = BASE_URL + ':8000'
SERVICE_URL = UI_URL + '/api/'


class TestStatuses(unittest.TestCase):

    def test_service_status(self):
        res = requests.get(SERVICE_URL)
        res.raise_for_status()

    def test_ui_status(self):
        res = requests.get(UI_URL)
        res.raise_for_status()
