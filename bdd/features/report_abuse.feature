Feature: Report Abuse
    As a registered user
    I want to report another user for inappropriate behaviour
    So that I can feel safe

    Background: There are two users in the database
        Given there are two standard users in the database
        And I am logged in as the first standard user

    Scenario Outline: User submits abuse report form
        Given I am "a logged in user"
        When I click on "Report Abuse" on another member's card
        And I enter "<comment>" into the "comments" field
        And I submit the form
        Then I see "<message>"

        Examples:
            |   comment     |   message                             |
            |   ""          |   Please describe your complaint.     |
            |   comments    |   Your Abuse Report has been logged   |
