Feature: Update Email

    Scenario: User views page
        Given I am an authenticated user
        When I visit the update email page
        Then I see the update email form
        And the form is populated with my email

    Scenario: User submits invalid data to the update email form
        Given I am an authenticated user
        And my current email is 'my.email@test.test'
        And my current password is 'pass'
        And 'taken.email@test.test' is already registered with another user
        When I input <email>
        And I input <password>
        And I submit the form
        Then I should see <error>

        Examples:
            |   email                   |   password    |   error                                                               |
            |   ''                      |   pass        |   This field is required.                                             |
            |   notarealemail           |   pass        |   Enter a valid email address.                                        |
            |   taken.email@test.test   |   pass        |   Sorry, this email address is already registered to another user.    |
            |   new.email@test.test     |   ''          |   This field is required.                                             |
            |   new.email@test.test     |   wrongpass   |   Incorrect password. Please try again.                               |

    Scenario: User updates their email
        Given I am an authenticated user
        When I input a new, valid email
        And this email is not registerd to another user
        And I input my password
        And I submit the form
        Then I should see "Your Connect email has been updated."

