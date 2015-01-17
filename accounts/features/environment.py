# Used with Behave to define code to run before and after certain events during BDD testing.
import factory
from behave import *
from splinter.browser import Browser

from accounts.factories import (InvitedPendingFactory, UserFactory, RoleFactory,
                                SkillFactory)
from connect_config.factories import SiteConfigFactory

def before_all(context):
    context.browser = Browser()
    context.server_url = 'http://localhost:8081/' # Django's default LiveServerTestCase port

    # Setup roles
    factory.create_batch(RoleFactory, 3)

    # Setup skills
    factory.create_batch(SkillFactory, 3)

    # Setup Users
    active_user = UserFactory(first_name='Active',
                              last_name='User1',
                              email='active.user1@test.test')

    inactive_user = InvitedPendingFactory(first_name='Inactive',
                                          last_name='User2',
                                          email='inactive.user2@test.test',
                                          auth_token='7891011')

    closed_user = UserFactory(first_name='Closed',
                              last_name='User3',
                              email='closed.user2@test.test',
                              is_closed=True)

def after_all(context):
    context.browser.quit()
    context.browser = None

