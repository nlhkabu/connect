Feature: Update Password

    Scenario: User views page
        Given I am an authenticated user
        When I visit the update password page
        Then I see the update password form

    Scenario Outline: User submits invalid data to the update password form
        Given I am an authenticated user
        And my current password is 'pass'
        When I input <new pass>
        And I input <current pass>
        And I submit the form
        Then I should see <error>

        Examples:
            |   new pass    |   current pass    |   error                                   |
            |   ''          |   pass            |   This field is required.                 |
            |   newpass     |   ''              |   This field is required.                 |
            |   newpass     |   wrongpass       |   Incorrect password. Please try again.   |

    Scenario: User updates their password
        Given I am an authenticated user
        When I input a new password
        And I input my current password
        And I submit the form
        Then I should see "Your Connect password has been updated."
