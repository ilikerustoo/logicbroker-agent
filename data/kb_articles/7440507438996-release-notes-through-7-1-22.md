---
title: "Release Notes Through 7/1/22"
url: "https://support.logicbroker.com/kb/logicbroker/7440507438996-release-notes-through-7-1-22"
category: "Logicbroker Updates"
---

March 3, 2026

# Release Notes Through 7/1/22

## 

## Portal Updates:

  * Shipments: 
    * Edit shipment is only allowed if the shipment is failed and not in any other status.
    * Don't block partial shipments with cancelled quantity
  * Product 
    * Added a new column type "Vendor Number" to the feed specification using the setting on the inventory feed page
    * Support for mapping rules on product feeds which apply to all feeds a retailer receives and runs after we add vendor number and map categories, before the items are validated.
    * Added method for extracting aspects/attributes for catalog mapping
    * Added method for finding or replacing attributes for catalog mapping
    * Ability for users to set up rules on catalog export templates and create new columns that will be exposed to the mappings.
    * Ability to import/export catalog export profiles
  * Notifications 
    * Provide partner breakdown for new document notifications.
    * Added event name to the email footer where it used to say just "notification". This is to help users determine which setting controls the notification.
    * Support for filter rules on email notifications to allow or block events by event type, partner, email subject and email body.
  * Scorecards: Ability to exclude weekends from shipment time
  * Failed Documents: EDI error messages have been shortened so details are easier to read.
  * Acknowledgement Settings: Support for the ability to use business days



## Connectors:

  * BigCommerce: 
    * Inventory Updates: Map Retail Price to Price, MSRP to Retail Price
    * Support for manual cancellation verification
    * Support for product variants
    * Ability to add custom fields to product feeds
  * ShipBob: 
    * Map invoice amount to handling amount for shipments
    * Trim leading zeros from line number in order map



## Fix:

  * Only check existing orders for duplicates when pulling from API.