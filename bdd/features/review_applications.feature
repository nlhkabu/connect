Feature: Review Applications
    As a moderator
    I want to review account applications
    So that I can control who is able to join the site

    Background: There is one pending user and a moderator in the database
        Given there is a pending user in the database
        And there is a moderator in the database
        And I am logged in as that moderator

    Scenario: View applications
        Given I am "a logged in moderator"
        When I visit the "review applications" page
        Then I see a list of pending applications

    Scenario Outline: Launch modal
        Given I am "a logged in moderator"
        When I visit the "review applications" page
        When I click on "<link>"
        Then a modal containing a "<form>" pops up

        Examples:
            |   link                |   form                |
            |   Approve Application |   Approve Application |
            |   Reject Application  |   Reject Application  |

    Scenario: Close review application modal
        Given I am "a logged in moderator"
        And I have launched the "approve application" modal
        When I click on the close button
        Then the modal closes

    Scenario: Moderator submits invalid data to the form
        Given I am "a logged in moderator"
        And I have launched the "approve application" modal
        When I leave the "comments" field blank
        And I submit the modal form
        Then I see "This field is required."

    @wip
    Scenario Outline: Moderator submits decision
        Given I am "a logged in moderator"
        And I have launched the "<modal name>" modal
        When I enter "comment" into the "comments" field
        And I submit the modal form
        Then I see "<message>"
        And "<user>" is removed from my list

        Examples:
            |   modal name             |   message                                                      |   user                        |
            |   Approve Application    |   Pending Approval's account application has been approved.    |   pending.approval@test.test  |
            |   Reject Application     |   Pending Approval's account application has been rejected.    |   pending.approval@test.test  |
