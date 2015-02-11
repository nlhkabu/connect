# Used with Behave to define code to run before and after certain events during BDD testing.
import factory
from behave import *
from splinter.browser import Browser

from django.contrib.sites.models import Site
from django.core import management
from django.core.exceptions import ObjectDoesNotExist

from accounts.factories import RoleFactory, SkillFactory
from accounts.models import CustomUser
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


def before_scenario(context, scenario):

    # Reset the database before each scenario
    management.call_command('flush', verbosity=0, interactive=False)

    # Then recreate our base data
    site = Site.objects.get(domain='example.com')

    try:
        site_config = SiteConfig.objects.get(site=site)
    except ObjectDoesNotExist:
        site_config = SiteConfigFactory(site=site)

    # Setup skills
    SkillFactory(name='skill1')
    SkillFactory(name='skill2')

    # Setup roles
    RoleFactory(name='role1')
    RoleFactory(name='role2')
    RoleFactory(name='role3')


def after_all(context):
    context.browser.quit()
    context.browser = None

