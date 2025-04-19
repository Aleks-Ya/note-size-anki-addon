#noinspection CucumberUndefinedStep
Feature: Collection size in Deck Browser

  @smoke @deck_browser
  Scenario: Show collection size in Deck Browser

    Given I opened Deck Browser
    Then Collection size is displayed
    Then Tooltip of Collection size is correct
    Then Tooltip of Midea size is correct
    Then Tooltip of Unused size is correct
    Then Tooltip of Trash size is correct
    Then Tooltip of Total size is correct

    When I click "Show details" button near to Unused size
    Then "Check Media" dialog has opened

    When I click "Show details" button near to Trash size
    Then "Check Media" dialog has opened

    When I click "Configuration" icon
    Then "Configuration dialog" has opened
    When I click "Cancel" button
    Then "Configuration dialog" has closed

