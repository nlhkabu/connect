# Used with Behave to define code to run before and after certain events during BDD testing.
import factory
from behave import *
from splinter.browser import Browser

from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from accounts.factories import (InvitedPendingFactory, UserFactory, RoleFactory,
                                SkillFactory)

from connect_config.factories import SiteConfigFactory
from connect_config.models import SiteConfig


def before_all(context):

    #Unless specified, set our default browser to PhantomJS
    if context.config.browser:
        context.browser = Browser(context.config.browser)
    else:
        context.browser = Browser('phantomjs')

    # When we're running with PhantomJS we need to specify the window size.
    # This is a workaround for an issue where PhantomJS cannot find elements
    # by text - see: https://github.com/angular/protractor/issues/585
    if context.browser.driver_name == 'PhantomJS':
        context.browser.driver.set_window_size(1280, 1024)

    # Django's default LiveServerTestCase port
    context.server_url = 'http://localhost:8081/'


    # This data is going to be used across multiple features/scenarios
    # so it's better to set them up once here
    site = Site.objects.get(domain='example.com')

    try:
        site_config = SiteConfig.objects.get(site=site)
    except ObjectDoesNotExist:
        site_config = SiteConfigFactory(site=site)

    # Setup skills
    SkillFactory(name='testskill1')
    SkillFactory(name='testskill2')
    SkillFactory(name='testskill3')
    #factory.create_batch(SkillFactory, 3)

    # Setup Users
    active_user = UserFactory(first_name='Active',
                              last_name='User',
                              email='active.user@test.test',
                              auth_token='123456')

    inactive_user = InvitedPendingFactory(first_name='Inactive',
                                          last_name='User',
                                          email='inactive.user@test.test',
                                          auth_token='7891011')

    user_to_close = UserFactory(first_name='Close',
                                last_name='Me',
                                email='close.my.account@test.test')

    user_to_update_email = UserFactory(first_name='Update',
                                       last_name='My email',
                                       email='update.my.email@test.test')

    user_to_update_password = UserFactory(first_name='Update',
                                          last_name='My Password',
                                          email='update.my.password@test.test')

    closed_user = UserFactory(first_name='Closed',
                              last_name='User',
                              email='closed.user@test.test',
                              is_active=False,
                              is_closed=True)


def before_feature(context, feature):

    def login(email):
        context.browser.visit(context.server_url + 'accounts/login/')
        context.browser.fill('username', email)
        context.browser.fill('password', 'pass')
        context.browser.find_by_css('.submit').first.click()

    if 'login_close_user' in feature.tags:
        login('close.my.account@test.test')
    elif 'login_email_user' in feature.tags:
        login('update.my.email@test.test')
    elif 'login_pass_user' in feature.tags:
        login('update.my.password@test.test')
    elif 'login_std_user' in feature.tags:
        login('active.user@test.test')


def after_feature(context, feature):
    if 'logout' in feature.tags:
        context.browser.find_link_by_text('Logout').first.click()


def after_all(context):
    context.browser.quit()
    context.browser = None

