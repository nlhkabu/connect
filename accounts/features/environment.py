# Used with Behave to define code to run before and after certain events during BDD testing.
import factory
from behave import *
from splinter.browser import Browser

from accounts.factories import (InvitedPendingFactory, UserFactory, RoleFactory,
                                SkillFactory)

def before_all(context):
    context.browser = Browser()
    context.server_url = 'http://localhost:8081/' # Django's default LiveServerTestCase port

    # This data is going to be used across multiple scenarios
    # so it's better to set them up once here

    # Setup roles
    RoleFactory(name='testrole1')

    # Setup skills
    SkillFactory(name='testskill1')
    SkillFactory(name='testskill2')
    SkillFactory(name='testskill3')
    #factory.create_batch(SkillFactory, 3)

    # Setup Users
    active_user = UserFactory(first_name='Active',
                              last_name='User1',
                              email='active.user1@test.test',
                              auth_token='123456')

    inactive_user = InvitedPendingFactory(first_name='Inactive',
                                          last_name='User2',
                                          email='inactive.user2@test.test',
                                          auth_token='7891011')

    user_to_close = UserFactory(first_name='Close',
                                last_name='Me',
                                email='close.my.account@test.test',
                                is_active=False,
                                is_closed=True)

    user_to_update_email = UserFactory(first_name='Update',
                                       last_name='My email',
                                       email='update.my.email@test.test')

    closed_user = UserFactory(first_name='Closed',
                              last_name='User3',
                              email='closed.user3@test.test',
                              is_active=False,
                              is_closed=True)


def after_tag(context, tag):
    if tag == 'logout':
        context.browser.find_link_by_text('Logout').first.click()



def after_all(context):
    context.browser.quit()
    context.browser = None

