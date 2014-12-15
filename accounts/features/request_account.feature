Feature: Request Account

    Background: There are at least two users in the database
        Given the following users exist:
            |   first name  |   last name   |   email               |   closed  |
            |   User        |   One         |   user.one@test.test  |   false   |
            |   User        |   Two         |   user.two@test.test  |   true    |


    Scenario Outline: User submits invalid data to the request account form
        Given I am an unauthenticated user
        When I input <first name>
        And I input <last name>
        And I input <email>
        And I input <comments>
        And I submit the form
        Then I see <error>

        Examples:
            |   first name  |   last name   |    email                  |   comments    |   error                                                                   |
            |   ''          |   last        |    my.email@test.test     |   comment     |   This field is required.                                                 |
            |   first       |   ''          |    my.email@test.test     |   comment     |   This field is required.                                                 |
            |   first       |   last        |    ''                     |   comment     |   This field is required.                                                 |
            |   first       |   last        |    my.email@test.test     |   ''          |   This field is required.                                                 |
            |   first       |   last        |    invalidemail           |   comment     |   Please enter a valid email address.                                     |
            |   first       |   last        |    user.two@test.test     |   comment     |   Sorry, this email address is already registered to another user.        |
            |   first       |   last        |    user.one@test.test     |   comment     |   This email address is already registered to another (closed) account.   |


    Scenario: User cancels attempt to request new account
        Given I am an unauthenticated user
        When I click on the 'cancel' button
        Then I am taken back to the login page

    Scenario: User requests a new account
        Given I am an unauthenticated user
        When I input my first name
        And I input my last name
        And I input my unique email
        And I input comments
        And I submit the form
        Then I see 'Your request for an account has been sent'
