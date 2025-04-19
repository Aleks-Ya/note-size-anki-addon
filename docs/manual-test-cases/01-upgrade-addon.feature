#noinspection CucumberUndefinedStep
Feature: Upgrade addon from previous version

  @smoke
  Scenario: Install addon over previous version

    Given I deleted addon
    And I installed previous version by ID 1188705668
    And I restarted Anki
    And I installed latest version from file
    And I restarted Anki
    Then Anki started without errors
