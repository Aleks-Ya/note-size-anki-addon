#noinspection CucumberUndefinedStep
Feature: Use Windows OS

  @S1101 @smoke @browser @editor
  Scenario: Run addon on Windows 11

    Given I deleted addon
    And I installed previous version by ID 1188705668
    And I restarted Anki
    And I installed latest version from file
    And I restarted Anki
    Then Anki started without errors
