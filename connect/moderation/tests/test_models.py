from django.test import TestCase

from connect.moderation.factories import LogFactory

class ModerationLogMsgTest(TestCase):
    def test_string_method(self):
        msg = LogFactory(comment='My comment')

        self.assertEqual(msg.__str__(), 'Invitation: My comment')
