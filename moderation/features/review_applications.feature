Feature: Review Applications

    Background: The following user exists:
            |   first name  |   last name   |   email               |   active  |   requested invitation    |
            |   User        |   One         |   user.one@test.test  |   false   |   true                    |

    Scenario: View applications
        Given I am an authenticated moderator
        When I visit the review applications page
        Then I see a list of pending applications

    Scenario: Launch modal
        Given I am an authenticated moderator
        When I click on <link>
        Then a modal containing a <form> pops up

        Examples:
            |   link                |   form                |
            |   approve application |   Approve Application |
            |   reject application  |   Reject Application  |

    Scenario: Close modal
        Given I am a logged in moderator
        And I have launched the a modal
        When I click on the close button
        Then the modal closes

    Scenario: Moderator submits invalid data to the form
        Given I am a logged in moderator
        And I have launched the approve application modal
        When I input nothing in the comments box
        And I submit the form
        Then I see 'This field is required.'

    Scenario: Moderator submits decision
        Given I am a logged in moderator
        And I have launched the <modal>
        When I input a comment
        And I submit the form
        Then I see <message>
        And the application is removed from my abuse reports list

        Examples:
            |   modal                  |   message
            |   Approve Application    |   User One's account application has been approved.    |
            |   Reject Application     |   User One's account application has been rejected.    |
