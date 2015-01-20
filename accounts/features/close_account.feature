Feature: Close Account

    Scenario: User views page
        Given I am an authenticated user wanting to close my account
        When I visit the close account page
        Then I see the close account form

    Scenario Outline: User submits invalid data to the close account form
        Given I am an authenticated user wanting to close my account
        When I visit the close account page
        And I input <pass> into the password field
        And I submit the form
        Then I see <error>

        Examples:
            |   pass        |   error                                   |
            |   ""          |   "This field is required."               |
            |   "wrongpass" |   "Incorrect password. Please try again." |

    Scenario: User submits valid data
        Given I am an authenticated user wanting to close my account
        When I visit the close account page
        And I input "pass" into the password field
        And I submit the form
        Then I am redirected to a confirmation page
