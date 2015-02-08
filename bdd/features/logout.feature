Feature: Logout
    As a registered user
    I want to logout of my account
    So that I can keep my account secure

    Background: There is one active user in the database
        Given there is a standard, active user in the database
        And I am logged in as that standard user

    Scenario: User logs out
        Given I am "a logged in user"
        When I logout
        Then I am no longer authenticated
        And I am redirected to the login page
