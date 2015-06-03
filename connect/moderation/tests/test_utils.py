import datetime
import pytz

from django.test import TestCase
from django.utils import timezone

from connect.accounts.factories import UserFactory, ModeratorFactory

from connect.moderation.models import ModerationLogMsg
from connect.moderation.utils import log_moderator_event, get_date_limits


class LogMessageTest(TestCase):
    fixtures = ['group_perms']

    def test_can_log_moderation_event(self):
        msg_type = ModerationLogMsg.INVITATION
        user = UserFactory()
        moderator = ModeratorFactory()
        comment = 'This is my comment'

        log = log_moderator_event(
            msg_type=user,
            user=user,
            moderator=moderator,
            comment=comment
        )

        logs = ModerationLogMsg.objects.all()

        self.assertIn(log, logs)

    def test_date_limits_with_one_date(self):
        date = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)
        expected_start = datetime.datetime(2011, 8, 15, 0, 0, 0, 0, pytz.UTC)
        expected_end = datetime.datetime(2011, 8, 15, 23, 59, 59, 999999, pytz.UTC)

        start, end = get_date_limits(date)

        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_date_limits_with_two_dates(self):
        day_1 = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)
        day_2 = datetime.datetime(2011, 9, 1, 8, 15, 12, 0, pytz.UTC)

        expected_start = datetime.datetime(2011, 8, 15, 0, 0, 0, 0, pytz.UTC)
        expected_end = datetime.datetime(2011, 9, 1, 23, 59, 59, 999999, pytz.UTC)

        start, end = get_date_limits(day_1, day_2)

        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)

    def test_date_limits_with_non_UTC_timezone(self):
        london = pytz.timezone('Europe/London')
        # 1st August in London is equal to UTC+1 due to DST
        day = london.localize(datetime.datetime(2014, 8, 1, 8, 15, 12, 0))

        expected_start = datetime.datetime(2014, 7, 31, 23, 0, 0, 0, pytz.UTC)
        expected_end = datetime.datetime(2014, 8, 1, 22, 59, 59, 999999, pytz.UTC)

        start, end = get_date_limits(day)

        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)
