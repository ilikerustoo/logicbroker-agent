---
title: "Release Notes Through 6/3/22"
url: "https://support.logicbroker.com/kb/logicbroker/6786003452436-release-notes-through-6-3-22"
category: "Logicbroker Updates"
---

March 3, 2026

# Release Notes Through 6/3/22

## 

## Portal Updates:

  * Increased the portal invitation lifetime from 3 to 7 days 
  * AS2: Upgraded to self-signed certification to increase lifespan
  * CXML: Support multiple request types (orders, acknowledgments, shipments, invoices) through the API endpoint

  * Vendor Orders: Maps SKUs when sourcing by vendor number
  * Reporting: 
    * Support for row-level security 
    * Addition of scheduled ship date and estimated delivery date fields 
    * Ability to flag last modified date and ignored status for documents 
  * Payment Center: 
    * Transfers pending shipment are now shown on the Payment Center Dashboard 
    * Update for payout workflow to pay out transfers based on their last modified 



  * Help Center: Support for multiple knowledge bases when a company does not have its own but is linked to more than one partner



## Connectors:

  * ShipBob 
    * Support for ShipBob API 
    * Order Map Updates, Support for: 
      * Carrier Type

      * Payment Term

      * Shipping Method

      * Tags

      * Class Code Mapping

  * NetSuite 
    * Allow unlinked invoices to export to Logicbroker 
    * Support for quantity unit of measurement on invoices 
    * Rate will be added on PoAcks 
    * Addition of inventory saved search template 
  * Magento 2 
    * Support for inventory files containing lines more than 1000 characters long



## Fixes:

  * Updated over-refund detection logic



## Learn Logicbroker:

  * UI Enhancements 
    * Pop-out video player so the user can scroll through the page while the video continues to run 
    * Support for lightbox on images and videos
    * Addition of animations throughout the platform