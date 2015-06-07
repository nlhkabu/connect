from behave import given, when, then
from django.core import management
from connect.accounts.factories import (
    InvitedPendingFactory, ModeratorFactory, RequestedPendingFactory, UserFactory
)

DEFAULT_WAIT = 5


# Setting up our users
@given('there is a standard user in the database')
def impl(context):
    context.standard_user = UserFactory(full_name='Standard User',
                                        email='standard.user@test.test',
                                        auth_token='123456')

@given('there are two standard users in the database')
def impl(context):
    context.execute_steps('''
        given there is a standard user in the database
    ''')
    context.standard_user2 = UserFactory(full_name='Another User',
                                         email='standard.user2@test.test')

@given('there is an invited, but not yet active user in the database')
def impl(context):
    context.invited_user = InvitedPendingFactory(full_name='Inactive User',
                                                 email='inactive.user@test.test',
                                                 auth_token='7891011')

@given('there is a closed user in the database')
def impl(context):
    context.closed_user = UserFactory(full_name='Closed User',
                                      email='closed.user@test.test',
                                      is_active=False, is_closed=True)

@given('there is a moderator in the database')
def impl(context):
    management.call_command('loaddata', 'group_perms', verbosity=0)
    context.moderator = ModeratorFactory(full_name='Moderator User',
                                         email='moderator@test.test')

@given('there is a pending user in the database')
def impl(context):
    context.pending_user = RequestedPendingFactory(
        full_name='Pending Approval',
        email='pending.approval@test.test')

@given('I have invited a new member to the application')
def impl(context):
    context.execute_steps('''
        When I visit the "invite user" page
        And I enter "Invited User" into the "full name" field
        And I enter "invited.user@test.test" into the "email" field
        And I submit the form
    ''')


# Authentication
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
        'invite user': 'moderation/',
        'review applications': 'moderation/review-applications/',
        'abuse reports': 'moderation/review-abuse-reports/',
        'logs': 'moderation/logs/'
    }

    context.browser.visit(context.server_url + PAGE_URLS[page_name])


# Common Form Inputs
@when('I enter "{user_input}" into the "{field_name}" field')
def impl(context, user_input, field_name):

    if user_input == '""':
        user_input = ''

    FORMSET_FIELDS = {
        'first anchor': 'link-0-anchor',
        'first url': 'link-0-url',
        'second anchor': 'link-1-anchor',
        'second url': 'link-1-url'
    }

    if field_name in FORMSET_FIELDS:
        context.browser.fill(FORMSET_FIELDS[field_name], user_input)
    else:
        field_name = field_name.lower().replace(" ", "_")
        context.browser.fill(field_name, user_input)


@when('I select "{selection}" from the "{field_name}" dropdown')
def impl(context, selection, field_name):

    SKILL_FORMSET = {
        'first skill name': 'skill-0-skill',
        'first skill proficiency': 'skill-0-proficiency',
        'second skill name': 'skill-1-skill',
        'second skill proficiency': 'skill-1-proficiency',
    }

    if field_name in SKILL_FORMSET:
        field_name = SKILL_FORMSET[field_name]

    path = "//select[@name='{}']/option[text()='{}']".format(field_name,
                                                             selection)
    context.browser.find_by_xpath(path).click()



@when('I enter "{user_input}" into the modal "{field_name}" field')
def impl(context, user_input, field_name):

    if user_input == '""':
        user_input = ''

    context.browser.find_by_css('.ui-dialog').find_by_name(field_name).fill(user_input)

@when('I leave the "{field}" field blank')
def impl(context, field):
    pass



# Submitting the form
@when('I submit the form')
def impl(context):
    context.browser.find_by_css('form input[type=submit]').first.click()

@when('I submit the modal form')
def impl(context):
    context.browser.find_by_css('.ui-dialog.active form input[type=submit]').first.click()


# Modals
@then('the "{modal_name}" modal pops up')
def impl(context, modal_name):
    title = context.browser.find_by_css('.active .ui-dialog-title').value
    assert title == modal_name

@given('I have launched the "{modal_name}" modal')
def impl(context, modal_name):
    modal_name = modal_name.title()

    MODAL_PAGE_URLS = {
        'Approve Application': 'moderation/review-applications/',
        'Reject Application': 'moderation/review-applications/',
        'Resend Invitation': 'moderation/',
        'Revoke Invitation': 'moderation/',
        'Dismiss Report': 'moderation/review-abuse-reports/',
        'Warn User': 'moderation/review-abuse-reports/',
        'Ban User': 'moderation/review-abuse-reports/',
    }

    context.browser.visit(context.server_url + MODAL_PAGE_URLS[modal_name])
    context.browser.click_link_by_text(modal_name)

@when('I click on the close button')
def impl(context):
    context.browser.find_by_css('.active .ui-dialog-titlebar-close').click()

@then('the modal closes')
def impl(context):
    context.browser.is_element_not_present_by_css('.ui-dialog.active')


# Form Errors and Confirmation Messages
@then('I see "{message}"')
def impl(context, message):
    if not context.browser.is_text_present(message, wait_time=DEFAULT_WAIT):
        raise AssertionError('could not find {message!r} in page body:\n{body}'.format(
            message=message, body=context.browser.find_by_tag('body').text
        ))


# Clicking on an link by text
@when('I click on "{link_text}"')
def impl(context, link_text):
    context.browser.click_link_by_text(link_text)


# Common Redirects
@then('I am redirected to my dashboard')
def impl(context):
    assert 'Dashboard' in context.browser.title

@then('I am redirected to the login page')
def impl(context):
    assert 'Login' in context.browser.title
