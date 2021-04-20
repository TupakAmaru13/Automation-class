Feature: eBay Regression


  Background: Navigation
    Given Navigate to eBay

  Scenario: 1. Search bar verification for "dress"

    And In search bar type "dress"
    And Click "search" button
    Then All displayed items are relevant to keyword "dress"

  Scenario: 1.1 Search bar verification for "dress" on 40 pages

    And In search bar type "dress"
    And Click "search" button
    Then All displayed items on 5 pages are relevant to keyword "dress"

   Scenario: 1.2 Search bar verification for "pants"

     And In search bar type "pants"
     And Click "search" button
     Then All displayed items are relevant to keyword "pants"

   Scenario: 1.3 Search bar verification for "watch"

    And Search for "watch"
#    And Click "search" button
#    Then All displayed items are relevant to keyword "watch"


  Scenario: 2. Special characters check

    And In search bar type special characters
    And Click "search" button
    Then All categories displayed


  Scenario: 3. Upper and low cases check
     Given Navigate to eBay
     And In search bar type dress in low and upper case
     And Click "search" button
     Then All displayed items are relevant to keyword "dress"

  Scenario: 4. Empty search check
    Given Navigate to eBay
    And Click "search" button
    Then All categories displayed

  Scenario: 5. Search using keyboard "Enter"
    Given Navigate to eBay
    And In search bar type "dress"
    And Press Enter using keyboard
    Then All displayed items are relevant to keyword "dress"

  Scenario: 6. Click on Sell in navigation bar
    Given Navigate to eBay
    And Click "Sell" element
    Then List an item bar appears

  Scenario: 7. Click on My eBay in navigation bar
    Given Navigate to eBay
    And Click "My eBay" element
    Then User redirected to My ebay security page

  Scenario: 8. Click on Alert in navigation bar
    Given Navigate to eBay
    And Click "Notification" element
    Then Alert popup must be present

  Scenario Outline: 9. Verify that filter works
    Given Navigate to eBay
    And In search bar type "<search_term>"
    And Click "search" button
    Then Filter by "<chbx_label>" in category "<header>"
    Examples: All
    | search_term | header       | chbx_label |
    | shoes       | Features     | Breathable |
    | shoes       | Features     | Comfort    |
    | shoes       | Features     | Non-Slip   |
    | shoes       | Brand        | Nike       |
    | shoes       | Brand        | adidas     |
    | dress       | Dress Length | Short      |
    | dress       | Dress Length | Midi       |

  Scenario: 10. Multiple filter
     And In search bar type "shoes"
     And Click "search" button
     Then Filter by "adidas" in category "Brand"
     Then Filter by "Leather" in category "Upper Material"
     Then Filter by "Comfort" in category "Features"

  Scenario: 11. Multiple filter as a table
     And In search bar type "shoes"
     And Click "search" button
     Then Apply following filters
     | Filter         | value   |
     | Brand          | adidas  |
     | Upper Material | Leather |
     | Features       | Comfort |

  Scenario Outline: 11. Multiple filter as a table
     And In search bar type "<search_term>"
     And Click "search" button
     Then Apply following filters
     | Filter        | value          |
     | <filter_name> | <filter_value> |
     #Then Do the verification

    Examples: Shoes
    | search_term | filter_name | filter_value |
    | shoes       | Brand       | adidas       |
    | shoes       | Features    | Comfort      |

    Examples: Dress
    |search_term  | filter_name  | filter_value |
    | dress       | Dress Length | Short        |
    | dress       | Occasion     | Formal       |

    Examples: Pants
    | search_term | filter_name | filter_value |
    | pants       | Brand       | Nike         |
    | pants       | Size Type   | Regular      |


  Scenario: 13. Multiple filter - New test
     When In search bar type "shoes"
     And Click "search" button
     And Filter by "adidas" in category "Brand"
     And Filter by "Leather" in category "Upper Material"
     And Filter by "Comfort" in category "Features"
     Then Validate that all items related to following
       | Filter         | value   |
       | Brand          | adidas  |
       | Upper Material | Leather |
       | Features       | Comfort |
    
  Scenario: REMOVEME
    When test one page at "https://www.ebay.com/itm/Adidas-Cloudfoam-Advantage-Womens-Sneaker-Shoes/203024341651"
     | Filter         | value   |
     | Brand          | adidas  |
     | Upper Material | Leather |
     | Features       | Comfort |




