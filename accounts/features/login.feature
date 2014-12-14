Feature: Login

    Background: The database is set up and there is at least one active user
        Given that the site details have been configured
        And there is at least one active user in the database
        And that user's email is 'my.user@test.test'
        And that user's password is 'pass'

    Scenario: Invalid login
        Given I am a registered user
        When I input <email>
        And I input <password>
        And I submit the login form
        Then I see 'Your email and password didn't match. Please try again.'

        Examples:
            |   email               |   password    |
            |   ''                  |   pass        |
            |   my.user@test.test   |   ''          |
            |   my.user@test.test   |   wrongpass   |
            |   notanemail          |   pass        |

    Scenario: Valid Login
        Given I am a registered user
        When I input my email
        And I input my password
        And I submit the login form
        Then I am redirected to my dashboard
