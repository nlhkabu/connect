Feature: Request Account

    Scenario: User requests a new account
        Given I am an unauthenticated user
        When I request an invitation
        Then I see a confirmation message

    Scenario: No first name
        Given I am an unauthenticated user
        When I request an invitation
        But forget to enter my first name
        Then I see a validation message

    Scenario: No last name
        Given I am an unauthenticated user
        When I request an invitation
        But forget to enter my last name
        Then I see a validation message

    Scenario: No email address
        Given I am an unauthenticated user
        When I request an invitation
        But forget to enter my email address
        Then I see a validation message

    Scenario: Invalid email address
        Given I am an unauthenticated user
        When I request an invitation
        But I enter an invalid email
        Then I see a validation message

    Scenario: Unavailable email address
        Given I am an unauthenticated user
        When I request an invitation
        But I enter an email address already registered to another user
        Then I see a validation message

    Scenario: No comments
        Given I am an unauthenticated user
        When I request an invitation
        But forget to enter a comment
        Then I see a validation message

    Scenario: User cancels attempt to request new account
        Given I am an unauthenticated user
        When I click on the 'cancel' button
        Then I am taken back to the login page
