from behave import *

# Common to this feature
@when('I visit the login page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/login/')


@when('I login')
def impl(context):
    context.execute_steps('''
        when I visit the login page
        when I enter "active.user@test.test" into the "username" field
        when I enter "pass" into the "password" field
        when I submit the form
    ''')
