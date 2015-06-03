from django.http import Http404
from django.test import TestCase

from connect.accounts.factories import (InvitedPendingFactory, ModeratorFactory,
                                RequestedPendingFactory, UserFactory)
from connect.moderation.forms import (FilterLogsForm, InviteMemberForm,
                              ReInviteMemberForm, RevokeInvitationForm)


class TestInviteMemberForm(TestCase):
    def setUp(self):
        self.existing_user = UserFactory(email='existing.email@test.test')

    def form_data(self, email):
        return InviteMemberForm(data={
            'first_name': 'First',
            'last_name': 'Fast',
            'email': email,
        })

    def test_unregistered_email(self):
        form = self.form_data(email='brand.new.email@test.test')

        self.assertTrue(form.is_valid())

    def test_registered_email(self):
        form = self.form_data(email='existing.email@test.test')

        self.assertFalse(form.is_valid())


class TestReInviteMemberForm(TestCase):
    def setUp(self):
        self.moderator = ModeratorFactory()
        self.another_moderator = ModeratorFactory()

        self.invited_user = InvitedPendingFactory(
            email='existing.email@test.test',
            moderator=self.moderator,
        )

        self.user_invited_by_another_moderator = InvitedPendingFactory(
            moderator=self.another_moderator,
        )

        self.requested_user = RequestedPendingFactory(
            moderator=self.moderator,
        )

    def form_data(self, email='', user_id=''):
        if not email:
            email = self.invited_user.email

        if not user_id:
            user_id = self.invited_user.id

        return ReInviteMemberForm(
            moderator=self.moderator,
            data={
                'email': email,
                'user_id': user_id,
            }
        )

    def test_invalid_user_id_raises_404(self):
        """
        If we post to this form with an invalid (non-existatant) user ID, we
        should raise a 404.
        """
        form = self.form_data(user_id='897hyb')

        with self.assertRaises(Http404):
            form.is_valid()

    def test_user_who_has_not_been_invited_raises_404(self):
        """
        If we try to reinvite a user that has not been invited
        (i.e. they have requested an account), we should raise a 404.
        """
        user_id = self.requested_user.id
        form = self.form_data(user_id=user_id)

        with self.assertRaises(Http404):
            form.is_valid()

    def test_user_id_invited_by_another_moderator_raises_404(self):
        """
        If we try to reinvite a user that ANOTHER moderator has invited,
        i.e. by manually overriding the user_id, we should raise a 404.
        """
        user_id = self.user_invited_by_another_moderator.id
        form = self.form_data(user_id=user_id)

        with self.assertRaises(Http404):
            form.is_valid()

    def test_valid_data(self):
        form = self.form_data()

        self.assertTrue(form.is_valid())


class TestRevokeInvitationForm(TestCase):
    def test_valid_data(self):
        self.invited_user = InvitedPendingFactory(
            email='existing.email@test.test',
        )

        form = RevokeInvitationForm(
            data={
                'confirm': True,
                'user_id': self.invited_user.id,
            }
        )

        self.assertTrue(form.is_valid())


class TestFilterLogsForm(TestCase):
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
