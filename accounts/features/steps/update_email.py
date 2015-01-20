from behave import *

# Common to this feature
@given('I am an active authenticated user wanting to change my email')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/login/')
    context.browser.fill('username', 'update.my.email@test.test')
    context.browser.fill('password', 'pass')
    context.browser.find_by_css('.submit').first.click()


@when('I visit the update email page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/update/email/')

@when('I input "a.new.email@test.test" into the email field')
def impl(context):
    context.browser.fill('email', 'a.new.email@test.test')


# Unique to Scenario: User views page
@then('I see the update email form')
def impl(context):
    assert context.browser.find_by_css('.update-email').visible

@then('the email field is prepopulated with my email')
def impl(context):
    assert context.browser.find_by_name('email').value == 'update.my.email@test.test'


# Unique to Scenario: User updates their email
@then('I see "Your example.com email has been updated."')
def impl(context):
    assert context.browser.is_text_present(
        "Your example.com email has been updated.")

