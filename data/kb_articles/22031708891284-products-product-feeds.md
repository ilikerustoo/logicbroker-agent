---
title: "Products (Product Feeds)"
url: "https://support.logicbroker.com/kb/logicbroker/22031708891284-products-product-feeds"
category: "Supplier Onboarding"
---

March 10, 2026

# Products (Product Feeds)

## 

**Note** : You will need to upload/send a live product feed once you move to the production portal as feeds do not carry over from stage to production. 

### 

### **Review your partner's product specifications**

Review your retailer's product requirements from the **Product Feeds** page > **Feed Configuration** > **View feed specification**.

### **Create your product feed**

Download a template from the**[Product Feeds](https://stageportal.logicbroker.com/product-feeds)** page > **Upload** > **Download Template** > select **All categories** or a **specific category** depending on your assortment. 

### **Upload or send your product feed**

  * **Through the portal** : Upload your template file into the portal from the [**Product Feeds**](https://stageportal.logicbroker.com/product-feeds) page > **Upload**
  * **Through the API** : Use this endpoint to send a product feed: **[POST /api/v1/Product/{partnerId}](https://stage.commerceapi.io/swagger/ui/index#!/Product/Product_Upload)**
  * **Through SFTP/FTP** : Use this folder to send a product feed: **[/Product/Outbound](/kb/logicbroker/360022067631-SFTP-FTP?hsLang=en)**



**Note** : If you are connecting using another method such as AS2 or Shopify, you will need to manually upload your product feed through the portal.

### **Confirm your product feed was uploaded successfully**

In the portal, from the [**Product Feeds**](https://stageportal.logicbroker.com/product-feeds) page, go to **Feeds** > review the status of your upload. If you see:

  * **Pending** or **Complete** , you have successfully uploaded the product feed
  * **Failed** , download**** the report to see your errors in the first column,fix the errors and repeat the upload process