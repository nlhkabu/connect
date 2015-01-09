from behave import *

# Common to this feature
@when('I visit the update password page')
def impl(context):
    pass

@when('I input "newpass" into the new password field')
def impl(context):
    pass

@when('I input "pass" into the current password field')
def impl(context):
    pass


# Unique to Scenario: User views page
@then('I see the update password form')
def impl(context):
    pass


# Unique to Scenario Outline: User submits invalid data to the update password form
@when('I input "" into the new password field')
def impl(context):
    pass

@when('I input "" into the current password field')
def impl(context):
    pass

@when('I input "wrongpass" into the current password field')
def impl(context):
    pass


# Unique to Scenario: User updates their password
@then('I see "Your Connect password has been updated."')
def impl(context):
    pass

