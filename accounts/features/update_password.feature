Feature: Update Password

    Scenario: User views page
        Given I am an active authenticated user
        When I visit the update password page
        Then I see the update password form

    Scenario Outline: User submits invalid data to the update password form
        Given I am an active authenticated user
        When I visit the update password page
        And I input <new pass> into the new password field
        And I input <current pass> into the current password field
        And I submit the form
        Then I see <error>

        Examples:
            |   new pass    |   current pass    |   error                                   |
            |   ""          |   "pass"          |   "This field is required."               |
            |   "newpass"   |   ""              |   "This field is required."               |
            |   "newpass"   |   "wrongpass"     |   "Incorrect password. Please try again." |


        Given I am an active authenticated user
        When I visit the update password page
        When I input "newpass" into the new password field
        And I input "pass" into the current password field
        And I submit the form
        Then I see "Your Connect password has been updated."
