Feature: Activate Account

    Scenario: Invited user visits page to activate account
        Given I am an invited user
        When I visit my activation page
        Then I see the activate account form
        And the form is prepopulated with my first name and last name

    Scenario Outline: Invited user submits invalid data to the activate account form
        Given I am an invited user
        And I input <first name>
        And I input <last name>
        And I input <new pass>
        And I input <confirm pass>
        And I submit the form
        Then I see <error>

        Examples:
            |   first name  |   last name   |    new pass    |   confirm pass    |   error                                          |
            |   ''          |   last        |    pass        |   pass            |   This field is required.                        |
            |   first       |   ''          |    pass        |   pass            |   This field is required.                        |
            |   first       |   last        |    ''          |   pass            |   This field is required.                        |
            |   first       |   last        |    pass        |   ''              |   This field is required.                        |
            |   first       |   last        |    pass        |   notmatching     |   Your passwords do not match. Please try again. |

    Scenario: Invited user activates their account
        Given I am an invited user
        When I input my first name
        And I input my last name
        And I input my password
        And I confirm my password
        Then I am redirected to my dashboard
        And I see a welcome modal

    Scenario: Active user revisits page to activate account
        Given I am an active user
        When I visit my activation page
        Then I see "We're sorry, this activation token has already been used."
