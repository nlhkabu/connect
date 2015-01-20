from behave import *

# Common Users
@given('I am an inactive unauthenticated user')
def impl(context):
    # This user is already set up by our environment.py, so we can pass here
    pass

@given('I am an active authenticated user')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/login/')
    context.browser.fill('username', 'active.user1@test.test')
    context.browser.fill('password', 'pass')
    context.browser.find_by_css('.submit').first.click()

@given('I am an active unauthenticated user')
def impl(context):
    # This user is already set up by our environment.py, so we can pass here
    pass

@given('I am an unknown user')
def impl(context):
    pass


# Common Form Inputs

# First Name Fields
@when('I input "" into the first name field')
def impl(context):
    context.browser.fill('first_name', '')

@when('I input "First" into the first name field')
def impl(context):
    context.browser.fill('first_name', 'First')


# Last Name Fields
@when('I input "" into the last name field')
def impl(context):
    context.browser.fill('last_name', '')

@when('I input "Last" into the last name field')
def impl(context):
    context.browser.fill('last_name', 'Last')


# Email Fields
@when('I input "" into the email field')
def impl(context):
    context.browser.fill('email', '')

@when('I input "active.user1@test.test" into the email field')
def impl(context):
    context.browser.fill('email', 'active.user1@test.test')

@when('I input "inactive.user2@test.test" into the email field')
def impl(context):
    context.browser.fill('email', 'inactive.user2@test.test')

@when('I input "closed.user3@test.test" into the email field')
def impl(context):
    context.browser.fill('email', 'closed.user3@test.test')

@when('I input "invalidemail" into the email field')
def impl(context):
    context.browser.fill('email', 'invalidemail')


# Password Fields
@when('I input "" into the password field')
def impl(context):
    context.browser.fill('password', '')

@when('I input "pass" into the password field')
def impl(context):
    context.browser.fill('password', 'pass')

@when('I input "wrongpass" into the password field')
def impl(context):
    context.browser.fill('password', 'wrongpass')


# Submitting the form
@when('I submit the form')
def impl(context):
    context.browser.find_by_css('.submit').first.click()


# Common Form Errors
@then('I see "This field is required."')
def impl(context):
    assert context.browser.is_text_present('This field is required.')

@then('I see "Enter a valid email address."')
def impl(context):
    assert context.browser.is_text_present('Enter a valid email address.')

@then('I see "Sorry, this email address is already registered to another user."')
def impl(context):
    assert context.browser.is_text_present(
        'Sorry, this email address is already registered to another user.')

@then('I see "This email address is already registered to another (closed) account."')
def impl(context):
    assert context.browser.is_text_present(
        'This email address is already registered to another (closed) account.')

@then('I see "Incorrect password. Please try again."')
def impl(context):
    assert context.browser.is_text_present(
        'Incorrect password. Please try again.')


# Common Redirects
@then('I am redirected to my dashboard')
def impl(context):
    assert b'Dashboard' in context.browser.title

@then('I am redirected to the login page')
def impl(context):
    assert b'Login' in context.browser.title
