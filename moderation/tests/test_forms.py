from django.test import TestCase

from moderation.forms import FilterLogsForm


class TestFilterLogsFormValidation(TestCase):

    def test_validation_fails_if_custom_is_selected_but_both_dates_not_set(self):
        form = FilterLogsForm(data={
            'msg_type': 'ALL',
            'period': FilterLogsForm.CUSTOM,
        })

        self.assertFalse(form.is_valid())

    def test_validation_fails_if_custom_is_selected_but_start_date_not_set(self):
        form = FilterLogsForm(data={
            'msg_type': 'ALL',
            'period': FilterLogsForm.CUSTOM,
            'end_date': '02/10/2014',
        })

        self.assertFalse(form.is_valid())

    def test_validation_fails_if_custom_is_selected_but_end_date_not_set(self):
        form = FilterLogsForm(data={
            'msg_type': 'ALL',
            'period': FilterLogsForm.CUSTOM,
            'start_date': '01/10/2014',
        })

        self.assertFalse(form.is_valid())

    def test_validation_passes_if_custom_is_selected_and_dates_set(self):
        form = FilterLogsForm(data={
            'msg_type': 'ALL',
            'period': FilterLogsForm.CUSTOM,
            'start_date': '01/10/2014',
            'end_date': '02/10/2014',
        })

        self.assertTrue(form.is_valid())
