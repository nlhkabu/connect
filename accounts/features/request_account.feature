Feature: Request Account

    Scenario Outline: User submits invalid data to the request account form
        Given I am an unknown user
        When I visit the request account page
        And I input <first name> into the first name field
        And I input <last name> into the last name field
        And I input <email> into the email field
        And I input <comments> into the comments field
        And I submit the form
        Then I see <error>

        Examples:
            |   first name  |   last name   |    email                          |   comments    |   error                                                                   |
            |   ""          |   "Last"      |    "request.account@test.test"    |   "comment"   |   "This field is required."                                               |
            |   "First"     |   ""          |    "request.account@test.test"    |   "comment"   |   "This field is required."                                               |
            |   "First"     |   "Last"      |    ""                             |   "comment"   |   "This field is required."                                               |
            |   "First"     |   "Last"      |    "request.account@test.test"    |   ""          |   "This field is required."                                               |
            |   "First"     |   "Last"      |    "invalidemail"                 |   "comment"   |   "Enter a valid email address."                                          |
            |   "First"     |   "Last"      |    "active.user1@test.test"       |   "comment"   |   "Sorry, this email address is already registered to another user."      |
            |   "First"     |   "Last"      |    "closed.user3@test.test"       |   "comment"   |   "This email address is already registered to another (closed) account." |

    Scenario: User cancels attempt to request new account
        Given I am an unknown user
        When I visit the request account page
        And I cancel the request account form
        Then I am redirected to the login page

    Scenario: User requests a new account
        Given I am an unknown user
        When I visit the request account page
        And I input "First" into the first name field
        And I input "Last" into the last name field
        And I input "request.account@test.test" into the email field
        And I input "comment" into the comments field
        And I submit the form
        Then I see "Your request for an account has been sent"
