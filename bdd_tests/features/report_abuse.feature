Feature: Report Abuse

    Background: The database is set up with two active users

    Scenario: User reports another user
        Given I am an authenticated user
        When I click on the link to report another user
        And I fill out the comments
        Then I see a confirmation message

    Scenario: User attempts to report another user without comments
        Given I am an authenticated user
        When I click on the link to report another user
        But I forget to fill out the comments
        Then I see a validation message
