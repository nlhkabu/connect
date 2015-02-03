from behave import *
from splinter.exceptions import ElementDoesNotExist

# Users
@given('I am "{user_type}"')
def impl(context, user_type):
    # Users are set up (and logged in, if applicable) by our
    # environment.py, so we can pass here
    pass


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


# Submitting the form
@when('I submit the form')
def impl(context):
    context.browser.find_by_css('.submit').first.click()


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
