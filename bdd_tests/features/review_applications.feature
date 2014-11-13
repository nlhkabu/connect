Feature: Review Applications

    Scenario: View applications
        Given I am an authenticated moderator
        When I visit the review applications page
        Then I see a list of pending applications

    Scenario: Approve application
        Given I am an authenticated moderator
        When I approve an application
        Then the application is removed from the list

    Scenario: No comment for approval
        Given I am an authenticated moderator
        When I approve an application
        But I do not provide a comment
        Then I see an error message

    Scenario: Reject application
        Given I am an authenticated moderator
        When I reject an application
        Then the application is removed from the list

    Scenario: No comment for rejection
        Given I am an authenticated moderator
        When I reject an application
        But I do not provide a comment
        Then I see an error message
