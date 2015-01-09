from behave import *

# Common to this feature
@when('I visit the update email page')
def impl(context):
    pass

@when('I input "a.new.email@test.test" into the email field')
def impl(context):
    pass


# Unique to Scenario: User views page
@then('I see the update email form')
def impl(context):
    pass

@then('the email field is prepopulated with my email ("active.user1@test.test")')
def impl(context):
    pass


# Unique to Scenario: User updates their email
@then('I see "Your Connect email has been updated."')
def impl(context):
    pass
