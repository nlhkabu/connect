Feature: Moderate Abuse Reports
    As a moderator
    I want to review the abuse reports
    So that I can ensure the safety of all of the site's users

    Background: The database is set up with several abuse reports
        Given there are two standard users in the database
        And there is a moderator in the database
        And I am logged in as that moderator
        And the second user has logged a complaint against the first
        And the first standard user also has a prior warning
        And there has been a complaint logged against me

    Scenario: Visit abuse report page
        Given I am "a logged in moderator"
        When I visit the "abuse reports" page
        Then I see a list of abuse reports
        And I see existing warnings
        But I cannot see reports relating to myself

    Scenario: View prior warnings
        Given I am "a logged in moderator"
        When I visit the "abuse reports" page
        When I click on the prior warnings link
        Then I see the proir warnings modal, with information inside it

    Scenario Outline: Launch form modal
        Given I am "a logged in moderator"
        When I visit the "abuse reports" page
        When I click on "<link>"
        Then the "<modal>" modal pops up

        Examples:
            |   link            |   modal                   |
            |   Dismiss Report  |   Dismiss Abuse Report    |
            |   Warn User       |   Warn User               |
            |   Ban User        |   Ban User                |

    Scenario: Close modal
        Given I am "a logged in moderator"
        And I have launched the "Dismiss Report" modal
        When I click on the close button
        Then the modal closes

    Scenario: Moderator does not provide a comment
        Given I am "a logged in moderator"
        And I have launched the "Dismiss Report" modal
        When I enter nothing in the comments field
        And I submit the modal form
        Then I see "Please explain your decision."

    Scenario Outline: Moderator submits decision
        Given I am "a logged in moderator"
        And I have launched the "<modal>" modal
        When I enter "comment" into the "comments" field
        And I submit the modal form
        Then I see "<message>"
        And the report is removed from my abuse reports list

        Examples:
            |   modal           |   message                                                 |
            |   Dismiss Report  |   The report against Standard User has been dismissed.    |
            |   Warn User       |   Standard User has been issued a formal warning.         |
            |   Ban User        |   Standard User has been banned from example.com.         |

