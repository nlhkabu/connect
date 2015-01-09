from behave import *

# Common Users
@given('I am an inactive unauthenticated user')
def impl(context):
    pass

@given('I am an active authenticated user')
def impl(context):

    #now I can login the active user I created in my before_all function...
    pass

@given('I am an active unauthenticated user')
def impl(context):
    pass

@given('I am an unknown user')
def impl(context):
    pass


# Common Form Inputs

# First Name Fields
@when('I input "" into the first name field')
def impl(context):
    pass

@when('I input "First" into the first name field')
def impl(context):
    pass


# Last Name Fields
@when('I input "" into the last name field')
def impl(context):
    pass

@when('I input "Last" into the last name field')
def impl(context):
    pass


# Email Fields
@when('I input "" into the email field')
def impl(context):
    pass

@when('I input "active.user1@test.test" into the email field')
def impl(context):
    pass

@when('I input "inactive.user2@test.test" into the email field')
def impl(context):
    pass

@when('I input "closed.user3@test.test" into the email field')
def impl(context):
    pass

@when('I input "invalidemail" into the email field')
def impl(context):
    pass


# Password Fields
@when('I input "" into the password field')
def impl(context):
    pass

@when('I input "pass" into the password field')
def impl(context):
    pass

@when('I input "wrongpass" into the password field')
def impl(context):
    pass


# Submitting the form
@when('I submit the form')
def impl(context):
    pass


# Common Form Errors
@then('I see "This field is required."')
def impl(context):
    pass

@then('I see "Please enter a valid email address."')
def impl(context):
    pass

@then('I see "Sorry, this email address is already registered to another user."')
def impl(context):
    pass

@then('I see "This email address is already registered to another (closed) account."')
def impl(context):
    pass

@then('I see "Incorrect password. Please try again."')
def impl(context):
    pass


# Common Redirects
@then('I am redirected to my dashboard')
def impl(context):
    pass

@then('I am redirected to the login page')
def impl(context):
    pass
