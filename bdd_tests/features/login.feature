Feature: Login

    Background: The database is set up and there is at least one active user
        Given that the site details have been configured
        And there is at least one active user in the database

    Scenario: Valid Login
        Given I am a registered user
        When I visit the login page
        And I put in a valid username and password
        Then I am redirected to the dashboard

    Scenario: Invalid email
        Given I am a registered user
        When I visit the login page
        But I put in an invalid email
        Then I am told that the email is invalid

    Scenario: Unregistered email
        Given I am a registered user
        When I visit the login page
        But I put in an unregistered email
        Then I am told that the email is unregistered

    Scenario: Incorrect Password
        Given I am a registered user
        When I visit the login page
        But I put in the incorrect password
        Then I am told that my password is incorrect
