from behave import *


# Common to this feature
@when('I visit my profile page')
def impl(context):
    pass


# Common form fields
@when('I input "My link1" into the first anchor field')
def impl(context):
    pass

@when('I input "http://myurl1.com" into the first URL field')
def impl(context):
    pass

@when('I input "My link2" into the second anchor field')
def impl(context):
    pass

@when('I input "http://myurl2.com" into the second URL field')
def impl(context):
    pass

@when('I select "skill1" for the first skill name field')
def impl(context):
    pass

@when('I select "BEGINNER" for the first skill proficiency field')
def impl(context):
    pass

@when('I select "skill2" for the second skill name field')
def impl(context):
    pass

@when('I select "EXPERT" for the second skill proficiency field')
def impl(context):
    pass


# Unique to Scenario: User views page
@then('I see the profile settings form')
def impl(context):
    pass

@then('the profile form is prepopulated with my data')
def impl(context):
    pass


# Unique to Scenario Outline: User submits invalid data to update profile form
@when('there are two link formsets showing')
def impl(context):
    pass

@when('there are two skill formsets showing')
def impl(context):
    pass

@when('I input "" into the first anchor field')
def impl(context):
    pass

@when('I input "" into the first URL field')
def impl(context):
    pass

@when('I input "My link1" into the second anchor field')
def impl(context):
    pass

@when('I input "http://myurl1.com" into the second URL field')
def impl(context):
    pass

@when('I select "" for the first skill name field')
def impl(context):
    pass

@when('I select "" for the first skill proficiency field')
def impl(context):
    pass

@when('I select "skill1" for the second skill name field')
def impl(context):
    pass

@then('I see "All links must have an anchor."')
def impl(context):
    pass

@then('I see "All links must have a url."')
def impl(context):
    pass

@then('I see "Links must have unique anchors and URLs."')
def impl(context):
    pass

@then('I see "All skills must have a skill name."')
def impl(context):
    pass

@then('I see "All skills must have a proficiency."')
def impl(context):
    pass

@then('I see "Each skill can only be entered once."')
def impl(context):
    pass


# Unique to Scenario: Biography field expands
@when('I add more than three lines to the biography field')
def impl(context):
    pass

@then('the field grows to accommodate the text')
def impl(context):
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
    pass

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
    pass

@then('another link formset is added to the bottom of the form')
def impl(context):
    pass


# Unique to Scenario: Update user's profile
@when('I input "my bio" into the bio field')
def impl(context):
    pass

@when('I check "role1"')
def impl(context):
    pass

@then('I see "Your profile has been updated"')
def impl(context):
    pass
