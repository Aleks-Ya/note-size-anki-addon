#noinspection CucumberUndefinedStep
Feature: Details Dialog functionality

  @smoke @browser @editor
  Scenario: Using Details Dialog

    Given I opened Browser
    And I clicked "Notes Size Button"
    Then "Detail Dialog" is displayed

    When I click "File" column
    Then Files are sorted by filename

    When I click "Size" column
    Then Files are sorted by size

    When I click "Configuration" icon
    Then "Configuration Dialog" has opened

    When I click "Close" button
    Then "Details Dialog" has closed
