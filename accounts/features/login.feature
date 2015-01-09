Feature: Login

    Scenario Outline: Invalid login
        Given I am an active unauthenticated user
        When I visit the login page
        And I input <email> into the email field
        And I input <password> into the password field
        And I submit the form
        Then I see "Your email and password didn't match. Please try again."

        Examples:
            |   email                       |   password    |
            |   ""                          |   "pass"      |
            |   "active.user1@test.test"    |   ""          |
            |   "active.user1@test.test"    |   "wrongpass" |
            |   "invalidemail"              |   "pass"      |

    Scenario: Valid Login
        Given I am an active unauthenticated user
        When I visit the login page
        And I input "active.user1@test.test" into the email field
        And I input "pass" into the password field
        And I submit the form
        Then I am redirected to my dashboard
