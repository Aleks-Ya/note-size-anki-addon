#noinspection CucumberUndefinedStep
Feature: Size of notes found in Browser

  @S0501 @smoke @browser
  Scenario: Show size of notes found in Browser

    Given I opened Browser
    And Browser is in notes mode
    And I searched for notes with query "deck:*"
    Then "Notes Size Button" is displayed

    When I clicked "Notes Size Button"
    Then "Progress Dialog" is displayed
    Then "Details Dialog" is displayed

    When I clicked "Notes Size Button" again
    Then Existing "Details Dialog" has closed
    Then New "Progress Dialog" is displayed
    Then New "Details Dialog" is displayed

    When I clicked Close button
    Then "Details Dialog" has closed

  @S0501 @smoke @browser
  Scenario: Show size of cards found in Browser

    Given I opened Browser
    And Browser is in cards mode
    And I searched for cards with query "deck:*"
    Then "Cards Size Button" is displayed

    When I clicked "Cards Size Button"
    Then "Progress Dialog" is displayed
    Then "Details Dialog" is displayed

    When I clicked "Cards Size Button" again
    Then Existing "Details Dialog" has closed
    Then New "Progress Dialog" is displayed
    Then New "Details Dialog" is displayed

    When I clicked Close button
    Then "Details Dialog" has closed