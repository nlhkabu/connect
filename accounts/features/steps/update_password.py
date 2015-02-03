from behave import *

# Common to this feature
@when('I visit the update password page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/update/password/')

