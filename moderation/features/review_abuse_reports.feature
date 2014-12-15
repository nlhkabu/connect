Feature: Review Abuse Reports

    Background: The database is set up with several abuse reports
        Given there are two standard users
        And a moderator
        And the standard users have logged abuse reports against each other

    Scenario: Visit abuse report page
        Given I am an authenticated moderator
        When I visit the abuse reports page
        Then I see a list of abuse reports
        And I can see existing warnings
        But I cannot see reports relating to myself

    Scenario Outline: Launch modal
        Given I am a logged in moderator
        When I click on <link>
        Then a modal containing a <form> pops up

        Examples:
            |   link            |   form                    |
            |   dismiss report  |   Dismiss Abuse Report    |
            |   warn user       |   Warn User               |
            |   ban user        |   Ban User                |

    Scenario: Close modal
        Given I am a logged in moderator
        And I have launched the a modal
        When I click on the close button
        Then the modal closes

    Scenario: Moderator submits invalid data to the form
        Given I am a logged in moderator
        And I have launched the dismiss report modal
        When I input nothing in the comments box
        And I submit the form
        Then I see 'This field is required.'

    Scenario Outline: Moderator submits decision
        Given I am a logged in moderator
        And I have launched the <modal> for the report logged against User One
        When I input a comment
        And I submit the form
        Then I see <message>
        And the report is removed from my abuse reports list

        Examples:
            |   modal                   |   message
            |   Dismiss Abuse Report    |   Abuse report dismissed.                     |
            |   Warn User               |   User One has been issued a formal warning.  |
            |   Ban User                |   User One has been banned from site.         |


