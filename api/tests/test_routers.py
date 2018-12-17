# -*- coding: utf-8 -*-
from django.test import TestCase


class RouterTest(TestCase):
    def test_get_request_does_not_redirect(self):
        response = self.client.options('/document/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_does_not_redirect_without_slash(self):
        response = self.client.options('/document')
        self.assertEqual(response.status_code, 200)
