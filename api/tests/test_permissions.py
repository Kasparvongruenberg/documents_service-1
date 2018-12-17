# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import RequestsClient


class RestFrameworkPermissionsTest(TestCase):
    def test_get_request_fails_without_auth(self):
        client = RequestsClient()
        client.headers.update({'x-test': 'true'})

        response = client.get('http://testserver/document/')
        assert response.status_code == 403

    def test_options_request_works_without_auth(self):
        client = RequestsClient()
        client.headers.update({'x-test': 'true'})

        response = client.options('http://testserver/document/')
        assert response.status_code == 200
