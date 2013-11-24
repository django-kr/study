from django.test import TestCase
import json


class FizzBuzzTest(TestCase):

    def response_should_success(self, response):
        self.assertEqual(response.status_code, 200)

    def cleaned_result(self, response):
        return response.content.replace(' ', '')

    def get_preset(self, max_range):
        preset = ['1', '2', '"fizz"', '4', '"buzz"', '6']
        result = '[' + \
            ','.join([x for x in preset[:max_range]]) + \
            ']'
        return result

    def test_when_input_in_1_to_6(self):
        for i in range(6):
            max_range = i + 1
            response = self.client.get('/fizz_buzz/?range=%d'
                                       % max_range)
            self.response_should_success(response)
            self.assertEqual(
                self.get_preset(max_range),
                self.cleaned_result(response)
            )
