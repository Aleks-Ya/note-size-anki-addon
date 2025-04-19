#noinspection CucumberUndefinedStep
Feature: Size of current note in Add Window

  @smoke @add
  Scenario: Show size of current note in Add Window

    Given I opened Add New Note Window
    Then Note size is zero

    When I type "hello"
    Then Note size is 5B

    When I copy "hello" to another field
    Then Note size is 10B

    When I click "Size Button"
    Then Details Dialog has opened
