#noinspection CucumberUndefinedStep
Feature: Size of current note in Add Window

  @S0301 @smoke @add
  Scenario: Show size of current note in Add Window

    Given I opened Add New Note Window
    Then Note size is zero

    When I type "hello"
    Then Note size is 5B

    When I copy "hello" to another field
    Then Note size is 10B

    When I click "Size Button"
    Then Details Dialog has opened
    Then Total notes size is 10B

    When I click "Size Button" again
    Then Existing Details Dialog has closed
    Then New Details Dialog has opened

    When I click Close button
    Then Details Dialog has closed