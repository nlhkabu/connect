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
