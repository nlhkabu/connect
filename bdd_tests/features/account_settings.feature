Feature: Account Settings

    Scenario: User views page
        Given I am an authenticated user
        When I visit the account settings page
        Then I see the account settings form, prepopulated with my data
        And I see the close account form, prepopulated with my email

    Scenario: Reset email address
        Given I am an authenticated user
        When I save a new email address
        Then this the new address is saved to my account

    Scenario: Attempt to save invalid email address
        Given I am an authenticated user
        When I try to save an invalid email address
        Then I see a validation message

    Scenario: Attempt to update setttings without email
        Given I am an authenticated user
        When I try to submit the 'Account Settings' form without an email address
        Then I see a validation message

    Scenario: Reset password
        Given I am an authenticated user
        When I input the current password
        And I input and confirm a new password
        Then my password is changed

    Scenario: Attempt to reset password without current password
        Given I am an authenticated user
        When I input and confirm a new password
        But forget to input the current password
        Then I see a validation message

    Scenario: Attempt to reset password with incorrect current password
        Given I am an authenticated user
        When I input and confirm a new password
        But incorrectly enter the current password
        Then I see a validation message

    Scenario: Attempt to reset password, without confirming new password
        Given I am an authenticated user
        When I input the current password
        And I input the new password
        But I do not confirm the password
        Then I see a validation message

    Scenario: Attempt to reset password, when new passwords do not match
        Given I am an authenticated user
        When I input the current password
        But the two new password fields do not match
        Then I see a validation message

    Scenario: Close account
        Given I am an authenticated user
        When I input the current password
        Then my account is closed and I am redirected to the homepage

    Scenario: Attempt to close account without current password
        Given I am an authenticated user
        When I try to close the account without the current password
        Then I see a validation message

    Scenario: Attempt to close account with incorrect current password
        Given I am an authenticated user
        When I try to close the account with an incorrect current password
        Then I see a validation message
