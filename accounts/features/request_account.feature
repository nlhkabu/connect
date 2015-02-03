Feature: Request Account

    Scenario Outline: User submits data to the request account form
        Given I am "an unknown user"
        When I visit the request account page
        And I enter "<first name>" into the "first name" field
        And I enter "<last name>" into the "last name" field
        And I enter "<email>" into the "email" field
        And I enter "<comments>" into the "comments" field
        And I submit the form
        Then I see "<message>"

        Examples:
            |   first name  |   last name   |   email                       |   comments    |   message                                                                 |
            |   ""          |   Last        |   request.account@test.test   |   comment     |   This field is required.                                                 |
            |   First       |   ""          |   request.account@test.test   |   comment     |   This field is required.                                                 |
            |   First       |   Last        |   ""                          |   comment     |   This field is required.                                                 |
            |   First       |   Last        |   request.account@test.test   |   ""          |   This field is required.                                                 |
            |   First       |   Last        |   invalidemail                |   comment     |   Enter a valid email address.                                            |
            |   First       |   Last        |   active.user@test.test       |   comment     |   Sorry, this email address is already registered to another user.        |
            |   First       |   Last        |   closed.user@test.test       |   comment     |   This email address is already registered to another (closed) account.   |
            |   First       |   Last        |   request.account@test.test   |   comment     |   Your request for an account has been sent                               |


    Scenario: User cancels attempt to request new account
        Given I am "an unknown user"
        When I visit the request account page
        And I cancel the request account form
        Then I am redirected to the login page
