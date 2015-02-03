from behave import *

# Common to this feature
@when('I visit the update email page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/update/email/')

# Unique to Scenario: User views page
@then('I see the update email form, prepopulated with my email')
def impl(context):
    assert context.browser.find_by_css('.update-email').visible
    assert context.browser.find_by_name('email').value == 'update.my.email@test.test'


