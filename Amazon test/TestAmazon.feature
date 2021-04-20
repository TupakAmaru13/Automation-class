Feature: Amazon
  Test Sales and Deals buttons

  Scenario Outline: Sales and deals buttons open appropriate pages
   When Navigate to Amazon
    Then Check all "<department>" deal buttons
    Examples: Super category
    |department|
    |Men's |
    |Women's|