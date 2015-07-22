from behave import *


# Unique to Scenario: User logs out
@when('I logout')
def impl(context):
    context.browser.find_link_by_text('Logout').first.click()

@then('I am no longer authenticated')
def impl(context):
    #Try to visit my profile page
    context.browser.visit(context.config.server_url + '/accounts/profile/')

    #But find that we're redirected to the login page
    assert context.browser.url == 'http://localhost:8081/accounts/login/?next=/accounts/profile/'
