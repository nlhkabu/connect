Feature: Profile Settings

    Background: The database is set up with an active user
        Given that the site details have been configured
        And there are skills in the database
        And there are roles in the database
        And the logged in user has a first name and last name

    Scenario: User views page
        Given I am an authenticated user
        When I visit the profile page
        Then I see the profile settings form, prepopulated with my data

    Scenario: Update user's name
        Given I am an authenticated user
        When I update my first name and last name
        Then my new name is saved

    Scenario: Attempt to submit profile form with no name
        Given I am an authenticated user
        When I try to submit the form without any information in either name field
        Then I see a validation message under each field

    Scenario: Biography field expands
        Given I am an authenticated user
        When I add more than three lines to the biography field
        Then the field 'grows' to accommodate the text

    Scenario: Save new biography
        Given I am an authenticated user
        When I add a biography
        Then my new biography is saved

    Scenario: Save roles
        Given I am an authenticated user
        When I select one or more roles
        Then the roles are saved to my profile

    Scenario: Save a new skill
        Given I am an authenticated user
        And 'django' is registered as a skill in the database
        When I select 'django' and 'beginner' from the skills form
        Then this skill is saved

    Scenario: No proficiency for a skill
        Given I am an authenticated user
        When I select a skill
        But I do not specify a proficiency
        Then I see an error message

    Scenario: No skill for a proficiency
        Given I am an authenticated user
        When I select a proficiency
        But I do not specify a skill
        Then I see an error message

    Scenario: Duplicate skill
        Given I am an authenticated user
        When I add the same skill twice
        Then I see an error message

    Scenario: Remove a form from the skills list
        Given I am an authenticated user
        When I click on 'remove' next to a skill form
        Then this form is removed from the list

    Scenario: Add another form to the skills list
        Given I am an authenticated user
        When I click on 'add skill'
        Then another skill formset is added to the bottom of the form

    Scenario: Save a new link
        Given I am an authenticated user
        When I add a valid anchor and URL
        Then the new link is saved

    Scenario: No URL for an anchor
        Given I am an authenticated user
        When I specify an anchor
        But do not specify a URL
        Then I see an error message

    Scenario: No anchor for a URL
        Given I am an authenticated user
        When I specify a URL
        But do not specify an anchor
        Then I see an error message

    Scenario: Duplicate anchor
        Given I am an authenticated user
        When I add the same anchor twice
        Then I see an error message

    Scenario: Duplicate URL
        Given I am an authenticated user
        When I add the same URL twice
        Then I see an error message

    Scenario: Invalid URL
        Given I am an authenticated user
        When I input an invalid URL
        Then I see an error message

    Scenario: Remove a form from the links list
        Given I am an authenticated user
        When I click on 'remove' next to a link form
        Then this form is removed from the list

    Scenario: Add another form to the links list
        Given I am an authenticated user
        When I click on 'add link'
        Then another link formset is added to the bottom of the form
