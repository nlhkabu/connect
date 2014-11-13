Feature: Activate Account

    Scenario: Invited user visits page to activate account
        Given I am an invited user
        When I visit my activation page
        Then I see a form prepopulated with my first name and last name

    Scenario: Invited user activates their account
        Given I am an invited user
        When I visit my activation page
        And I input my password
        And I confirm my password
        Then I am redirected to my dashboard
        And I see a welcome message

    Scenario: Invited user attempts to activate their account without first name
        Given I am an invited user
        When I try to activate my account
        But I forget to put in my first name
        Then I see a validation message

    Scenario: Invited user attempts to activate their account without last name
        Given I am an invited user
        When I try to activate my account
        But I forget to put in my last name
        Then I see a validation message

    Scenario: Invited user attempts to activate their account without password
        Given I am an invited user
        When I try to activate my account
        But I forget to put in my new password
        Then I see a validation message

    Scenario: Invited user attempts to activate their account without confirming password
        Given I am an invited user
        When I try to activate their account
        But I forget to confirm my new password
        Then I see a validation message

    Scenario: Invited user attempts to activate their account without matching passwords
        Given I am an invited user
        When I try to activate my account
        But my password and password confirmation do not match
        Then I see a validation message

    Scenario: Active user revisits page to activate account
        Given I am an active user
        When I visit my activation page
        Then I see that my activation key has been used
