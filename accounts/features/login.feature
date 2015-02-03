Feature: Login

    Scenario Outline: Invalid login
        Given I am "a logged out user"
        When I visit the login page
        And I enter "<email>" into the "username" field
        And I enter "<password>" into the "password" field
        And I submit the form
        Then I see "Your email and password didn't match. Please try again."

        Examples:
            |   email                   |   password    |
            |   ""                      |   pass        |
            |   active.user@test.test   |   ""          |
            |   active.user@test.test   |   wrongpass   |
            |   invalidemail            |   pass        |

    Scenario: Valid Login
        Given I am "a logged out user"
        When I login
        Then I am redirected to my dashboard
