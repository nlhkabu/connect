import datetime
import pytz

from django.utils import timezone

from .models import ModerationLogMsg


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


def get_date_limits(start_date, end_date=None, local_tz=None):
    """
    Return first and last UTC moments of given date(s),
    to the nearest microsecond.

    `start_date` and `end_date` can be naive or aware datetime or date objects.

    If only one date is specified, the first and last moments of this date
    will be returned.

    The default timezone (as specified in settings.py) will be used if none is
    specified.
    """
    if not end_date:
        end_date = start_date

    if not local_tz:
        local_tz = timezone.get_current_timezone()

    start = datetime.datetime.combine(start_date, datetime.time.min)
    start_aware = timezone.make_aware(start, local_tz)
    start_utc = start_aware.astimezone(pytz.UTC)

    end = datetime.datetime.combine(end_date, datetime.time.max)
    end_aware = timezone.make_aware(end, local_tz)
    end_utc = end_aware.astimezone(pytz.UTC)

    return (start_utc, end_utc)
