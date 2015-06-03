import datetime
import pytz

from django.utils import timezone

from connect.moderation.models import ModerationLogMsg


def log_moderator_event(msg_type, user, moderator, comment=''):
    """
    Log a moderation event.
    """
    message = ModerationLogMsg.objects.create(
        msg_type=msg_type,
        comment=comment,
        pertains_to=user,
        logged_by=moderator,
    )

    return message


def get_date_limits(start_date, end_date=None):
    """
    Return first and last UTC moments of given date(s),
    to the nearest microsecond.

    `start_date` and `end_date` must be aware datetime objects.

    If only one date is specified, the first and last moments of this date
    will be returned.
    """
    if not end_date:
        end_date = start_date

    start_date_tz = start_date.tzinfo
    end_date_tz = end_date.tzinfo

    start = datetime.datetime.combine(start_date, datetime.time.min)
    start_local = timezone.make_aware(start, start_date_tz)
    start_utc = start_local.astimezone(pytz.UTC)

    end = datetime.datetime.combine(end_date, datetime.time.max)
    end_local = timezone.make_aware(end, end_date_tz)
    end_utc = end_local.astimezone(pytz.UTC)

    return (start_utc, end_utc)
