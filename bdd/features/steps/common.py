import factory
from behave import *
from splinter.exceptions import ElementDoesNotExist
from django.core import management
from accounts.factories import (InvitedPendingFactory, ModeratorFactory,
                                RequestedPendingFactory, UserFactory)


# Users
@given('there is a standard user in the database')
def impl(context):
    UserFactory(first_name='Standard', last_name='User',
                email='standard.user@test.test', auth_token='123456')

@given('there are two standard users in the database')
def impl(context):
    context.execute_steps('''
        given there is a standard user in the database
    ''')
    UserFactory(first_name='Another', last_name='User',
                email='standard.user2@test.test')

@given('there is an invited, but not yet active user in the database')
def impl(context):
    InvitedPendingFactory(first_name='Inactive', last_name='User',
                          email='inactive.user@test.test', auth_token='7891011')

@given('there is a closed user in the database')
def impl(context):
    closed_user = UserFactory(first_name='Closed', last_name='User',
                              email='closed.user@test.test',
                              is_active=False, is_closed=True)

@given('there is a moderator in the database')
def impl(context):
    management.call_command('loaddata', 'group_perms', verbosity=0)
    moderator = ModeratorFactory(first_name='Moderator', last_name='User',
                                 email='moderator@test.test')

@given('there is a pending user in the database')
def impl(context):
    RequestedPendingFactory(first_name='Pending', last_name='Approval',
                            email='pending.approval@test.test')


#Logged in
@given('I am logged in as that standard user')
def impl(context):
    context.execute_steps('''
        when I visit the "login" page
        when I enter "standard.user@test.test" into the "username" field
        when I enter "pass" into the "password" field
        when I submit the form
    ''')

@given('I am logged in as that moderator')
def impl(context):
    context.execute_steps('''
        when I visit the "login" page
        when I enter "moderator@test.test" into the "username" field
        when I enter "pass" into the "password" field
        when I submit the form
    ''')

@given('I am logged in as the first standard user')
def impl(context):
    context.execute_steps('''
        given I am logged in as that standard user
    ''')

@given('I am "{user_type}"')
def impl(context, user_type):
    # Users are created (and logged in, if applicable) during our
    # background setup, so we can pass here
    pass


# URLs
@when('I visit the "{page_name}" page')
def impl(context, page_name):

    PAGE_URLS = {
        'close account': 'accounts/close/',
        'login': 'accounts/login/',
        'request account': 'accounts/request-invitation/',
        'reset password': 'accounts/password/reset/',
        'update email': 'accounts/update/email/',
        'update password': 'accounts/update/password/',
        'profile': 'accounts/profile/',
        'dashboard': '', # root url
        'invite user': 'moderation',
        'review applications': 'moderation/review-applications/',
    }

    context.browser.visit(context.server_url + PAGE_URLS[page_name])


# Common Form Inputs
@when('I enter "{user_input}" into the "{field_name}" field')
def impl(context, user_input, field_name):

    if user_input == '""':
        user_input = ''

    LINK_FORMSET = {
        'first anchor': 'link-0-anchor',
        'first url': 'link-0-url',
        'second anchor': 'link-1-anchor',
        'second url': 'link-1-url'
    }

    if field_name in LINK_FORMSET:
        context.browser.fill(LINK_FORMSET[field_name], user_input)
    else:
        field_name = field_name.lower().replace(" ", "_")
        context.browser.fill(field_name, user_input)

@when('I leave the "{field}" field blank')
def impl(context, field):
    pass


# Submitting the form
@when('I submit the form')
def impl(context):
    context.browser.find_by_css('form input[type=submit]').first.click()

@when('I submit the modal form')
def impl(context):
    context.browser.find_by_css('.ui-dialog form input[type=submit]').first.click()


# Form Errors and Confirmation Messages
@then('I see "{message}"')
def impl(context, message):
    assert context.browser.is_text_present(message, wait_time=30)


# Common Redirects
@then('I am redirected to my dashboard')
def impl(context):
    assert b'Dashboard' in context.browser.title

@then('I am redirected to the login page')
def impl(context):
    assert b'Login' in context.browser.title
