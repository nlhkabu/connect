Feature: Close Account

    Scenario: User views page
        Given I am an authenticated user
        When I visit the close account page
        Then I see the close account form

    Scenario: User submits invalid data to the close account form
        Given I am an authenticated user
        And my current password is 'pass'
        When I input <pass>
        And I submit the form
        Then I should see <error>

        Examples:
            |   pass        |   error                                  |
            |   ''          |   This field is required.                |
            |   wrongpass   |   Incorrect password. Please try again.  |

    Scenario: User submits valid data
        Given I am an authenticated user
        When I input my password
        And I submit the form
        Then I should be redirected to a confirmation page
