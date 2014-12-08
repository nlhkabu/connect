from django.test import TestCase

from moderation.forms import FilterLogsForm


class TestFilterLogsFormValidation(TestCase):

    def form_data(self, start='', end=''):
        return FilterLogsForm(data={
            'msg_type': 'ALL',
            'period': FilterLogsForm.CUSTOM,
            'start_date': start,
            'end_date': end,
        })

    def test_missing_both_dates(self):
        """
        Test validation fails is custom is selected but both dates are not set.
        """
        form = self.form_data()
        errors = form.errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors['__all__'][0].code, 'missing_date')

    def test_missing_start_date(self):
        """
        Test validation fails is custom is selected but start date is not set.
        """
        form = self.form_data(end='02/10/2014')
        errors = form.errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors['__all__'][0].code, 'missing_date')

    def test_missing_end_date(self):
        """
        Test validation fails is custom is selected but end date is not set.
        """
        form = self.form_data('02/10/2014')
        errors = form.errors.as_data()

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors['__all__'][0].code, 'missing_date')

    def test_valid_data(self):
        form = self.form_data('01/10/2014', '02/10/2014')

        self.assertTrue(form.is_valid())
