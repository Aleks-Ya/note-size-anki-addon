#noinspection CucumberUndefinedStep
Feature: Size columns in Browser

  @S0401 @smoke @browser @editor
  Scenario: Sort notes by size

    Given I opened Browser
    Then Column "Size" is displayed
    Then Column "Size (texts)" is displayed
    Then Column "Size (files)" is displayed

    When I click on header of "Size" column
    Then Notes are sorted by "Size" column descending
    When I click on header of "Size" column
    Then Notes are sorted by "Size" column ascending

    When I click on header of "Size (texts)" column
    Then Notes are sorted by "Size (texts)" column descending
    When I click on header of "Size (texts)" column
    Then Notes are sorted by "Size (texts)" column ascending

    When I click on header of "Size (files)" column
    Then Notes are sorted by "Size (files)" column descending
    When I click on header of "Size (files)" column
    Then Notes are sorted by "Size (files)" column ascending