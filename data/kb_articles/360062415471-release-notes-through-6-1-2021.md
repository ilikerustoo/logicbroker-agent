---
title: "Release Notes Through 6/1/2021"
url: "https://support.logicbroker.com/kb/logicbroker/360062415471-release-notes-through-6-1-2021"
category: "Logicbroker Updates"
---

March 3, 2026

# Release Notes Through 6/1/2021

## 

### Portal Updates:

  * **Scorecards:** Support for Vendor-based SLA Reporting
  * **Product Feeds** : Error column has been added for product feeds downloads
  * **Product Catalog:**
    * Support for category mapping through the manage categories feature
    * Warning for users if the catalog contains scientific notation when importing
    * Maximum product image size is set to 5 MB on all endpoints
  * **CCN** : Catalog items on the CCN profile page are now displayed using a tile format
  * **API:**
    * New endpoint for retrieving standard category taxonomy. The new endpoint is /api/v1/product/categories/taxonomy 
      * More information can be found in the API reference: <https://stage.commerceapi.io/swagger/ui/index#!/Product/Product_GetTaxonomy>
    * New endpoints for managing categories. The end points are

GET /api/v1/product/categories

POST /api/v1/product/categories/bulkupdate

POST /api/v1/product/categories/export

POST /api/v1/product/categories/import

      * More information can be found in the API references:

<https://stage.commerceapi.io/swagger/ui/index#!/Product/Product_GetAllCategories> <https://stage.commerceapi.io/swagger/ui/index#!/Product/Product_CreateOrUpdateCategories> <https://stage.commerceapi.io/swagger/ui/index#!/Product/Product_ExportCategories> <https://stage.commerceapi.io/swagger/ui/index#!/Product/Product_ImportCategories>



### Connector Updates:

  * **Shopify** : Ship to email added to the order map for the supplier flow
  * **ShipStation:** Item options are now mapped on the order 
  * **NetSuite** : Ability to apply NetSuite default addresses at a companywide level for sales orders