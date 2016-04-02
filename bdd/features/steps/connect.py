from behave import given, when, then
from django.core import management
from connect.accounts.factories import (
    InvitedPendingFactory, ModeratorFactory, RequestedPendingFactory, UserFactory
)

DEFAULT_WAIT = 5


# Setting up our users
@when('I click on the connect button of the second user')
def impl(context):
    context.browser.find_by_css('.connect-btn').click()


@then('I will be redirected to the connect page')
def impl(context):
    assert 'Contact Another User' in context.browser.title
