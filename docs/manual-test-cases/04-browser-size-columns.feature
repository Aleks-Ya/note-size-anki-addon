#noinspection CucumberUndefinedStep
Feature: Size columns in Browser

  @smoke @browser @editor
  Scenario: Sort notes by size

    Given I opened Browser
    Then Column "Size" is displayed
    Then Column "Size (texts)" is displayed
    Then Column "Size (files)" is displayed

    When I click on header of "Size" column
    Then Notes are sorted by size
    When I click on header of "Size" column
    Then Notes are sorted by size in opposite direction
