Feature: Close Account
    As a registered user
    I want to close my account
    So that I can use stop using this application

    Background: There is one user in the database
        Given there is a standard, active user in the database
        And I am logged in as that standard user

    Scenario Outline: User submits invalid data to the close account form
        Given I am "a logged in user"
        When I visit the "close account" page
        And I enter "<pass>" into the "password" field
        And I submit the form
        Then I see "<error>"

        Examples:
            |   pass        |   error                                   |
            |   ""          |   This field is required.                 |
            |   wrongpass   |   Incorrect password. Please try again.   |

    Scenario: User submits valid data
        Given I am "a logged in user"
        When I visit the "close account" page
        And I close my account
        Then I am redirected to a confirmation page
