Feature: Activate Account
    As an invited user
    I want to activate my account
    So that I can use this application

    Background: There are two users in the database
        Given there is a standard user in the database
        And there is an invited, but not yet active user in the database

    Scenario: Invited user visits page to activate account
        Given I am "an invited, but not active user"
        When I visit my activation page "7891011"
        Then I see the activate account form, prepopulated with my data

    Scenario Outline: Invited user submits invalid data to the activate account form
        Given I am "an invited, but not active user"
        When I visit my activation page "7891011"
        And I enter "<full name>" into the "full name" field
        And I enter "<new pass>" into the "password" field
        And I enter "<confirm pass>" into the "confirm password" field
        And I submit the form
        Then I see "<error>"

        Examples:
            |   full name   |    new pass   |   confirm pass    |   error                                           |
            |   ""          |    pass       |   pass            |   Please enter your full name.                    |
            |   First Last  |    ""         |   pass            |   Please select a password.                       |
            |   First Last  |    pass       |   ""              |   Please confirm your password.                   |
            |   First Last  |    pass       |   notmatching     |   Your passwords do not match. Please try again.  |

    Scenario: Invited user activates their account
        Given I am "an invited, but not active user"
        When I visit my activation page "7891011"
        And I activate my account
        Then I am redirected to my dashboard
        And I see a welcome modal

    Scenario: Active user revisits page to activate account
        Given I am "a logged out user"
        When I visit my activation page "123456"
        Then I see "We're sorry, this activation token has already been used."

