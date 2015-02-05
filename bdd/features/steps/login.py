from behave import *


@when('I login')
def impl(context):
    context.execute_steps('''
        when I visit the "login" page
        when I enter "active.user@test.test" into the "username" field
        when I enter "pass" into the "password" field
        when I submit the form
    ''')
