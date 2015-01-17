from behave import *


# Common to this feature
@when('I visit my profile page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/profile/')


# Common form fields
@when('I input "My link1" into the first anchor field')
def impl(context):
    context.browser.fill('link-0-anchor', 'My link1')

@when('I input "http://myurl1.com" into the first URL field')
def impl(context):
    context.browser.fill('link-0-url', 'http://myurl1.com')

@when('I input "My link2" into the second anchor field')
def impl(context):
    context.browser.fill('link-1-anchor', 'My link2')

@when('I input "http://myurl2.com" into the second URL field')
def impl(context):
    context.browser.fill('link-1-url', 'http://myurl2.com')

@when('I select "skill1" for the first skill name field')
def impl(context):
    context.browser.select('skill-0-skill', 'skill1')

@when('I select "BEGINNER" for the first skill proficiency field')
def impl(context):
    context.browser.select('skill-0-proficiency', 'beginner')

@when('I select "skill2" for the second skill name field')
def impl(context):
    context.browser.select('skill-1-skill', 'skill2')

@when('I select "EXPERT" for the second skill proficiency field')
def impl(context):
    context.browser.select('skill-1-proficiency', 'expert')


# Unique to Scenario: User views page
@then('I see the profile settings form')
def impl(context):
    assert context.browser.find_by_css('.profile-settings').visible

@then('the profile form is prepopulated with my data')
def impl(context):
    assert context.browser.find_by_name('first_name').value == 'Active'
    assert context.browser.find_by_name('last_name').value == 'User1'


# Unique to Scenario Outline: User submits invalid data to update profile form
@when('there are two link formsets showing')
def impl(context):
    context.browser.find_link_by_text('add link').first.click()

@when('there are two skill formsets showing')
def impl(context):
    context.browser.find_link_by_text('add skill').first.click()

@when('I input "" into the first anchor field')
def impl(context):
    context.browser.fill('link-0-anchor', '')

@when('I input "" into the first URL field')
def impl(context):
    context.browser.fill('link-0-url', '')

@when('I input "My link1" into the second anchor field')
def impl(context):
    context.browser.fill('link-1-anchor', 'My link1')

@when('I input "http://myurl1.com" into the second URL field')
def impl(context):
    context.browser.fill('link-1-url', 'http://myurl1.com')

@when('I select "" for the first skill name field')
def impl(context):
    context.browser.select('skill-0-skill', '')

@when('I select "" for the first skill proficiency field')
def impl(context):
    context.browser.select('skill-0-proficiency', '')

@when('I select "skill1" for the second skill name field')
def impl(context):
    context.browser.select('skill-1-skill', 'skill1')

@then('I see "All links must have an anchor."')
def impl(context):
    assert context.browser.is_text_present("All links must have an anchor.")

@then('I see "All links must have a url."')
def impl(context):
    assert context.browser.is_text_present("All links must have a url.")

@then('I see "Links must have unique anchors and URLs."')
def impl(context):
    assert context.browser.is_text_present(
        "Links must have unique anchors and URLs.")

@then('I see "All skills must have a skill name."')
def impl(context):
    assert context.browser.is_text_present(
        "All skills must have a skill name.")

@then('I see "All skills must have a proficiency."')
def impl(context):
    assert context.browser.is_text_present(
        "All skills must have a proficiency.")

@then('I see "Each skill can only be entered once."')
def impl(context):
    assert context.browser.is_text_present(
        "Each skill can only be entered once.")


# Unique to Scenario: Biography field expands
@when('I add more than three lines to the biography field')
def impl(context):
    context.browser.fill('bio', '\n\n\n\n\n\n\n')

@then('the field grows to accommodate the text')
def impl(context):

    field = context.browser.find_by_name('bio')
    #~print(field.size['height'])
    pass



# Unique to Scenario: Remove a form from the skills list
@when('I click on remove next to a skill form')
def impl(context):
    pass

@then('this skills formset is removed from the list')
def impl(context):
    pass


# Unique to Scenario: Add another form to the skills list
@when('I click on add skill')
def impl(context):
    context.browser.find_link_by_text('add skill').first.click()

@then('another skill formset is added to the bottom of the form')
def impl(context):
    pass


# Unique to Scenario: Remove a form form the links list
@when('I click on remove next to a link form')
def impl(context):
    pass

@then('this links formset is removed from the list')
def impl(context):
    pass


# Unique to Scenario: Add another form to the links list
@when('I click on add link')
def impl(context):
    context.browser.find_link_by_text('add link').first.click()

@then('another link formset is added to the bottom of the form')
def impl(context):
    pass


# Unique to Scenario: Update user's profile
@when('I input "my bio" into the bio field')
def impl(context):
    context.browser.fill('bio', 'my bio')

@when('I check "role1"')
def impl(context):
    context.browser.check('role1')

@then('I see "Your profile has been updated"')
def impl(context):
    assert context.browser.is_text_present("Your profile has been updated.")
