#noinspection CucumberUndefinedStep
Feature: Using earliest Anki version 24.4.1

  @smoke @browser @editor
  Scenario: Use in Anki 24.4.1

    Given I opened Anki 24.4.1 Qt5
    And I deleted addon
    And I installed previous version by ID 1188705668
    And I restarted Anki
    And I installed latest version from file
    And I restarted Anki
    Then Anki started without errors