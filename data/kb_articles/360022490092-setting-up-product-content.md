---
title: "Setting Up Product Content"
url: "https://support.logicbroker.com/kb/logicbroker/360022490092-setting-up-product-content"
category: "Supplier Onboarding"
---

March 6, 2026

# Setting Up Product Content

## 

Product Feeds are used to send product content data to **retailers/channels**. This includes product descriptions, attributes (size, color, specifications, etc.), image URLs and any data required by the **retailer/channel** to setup products to be listed on their platform. These channels can include marketplaces, eCommerce sites, product information management ( **PIM**) or digital asset management ( **DAM**) systems.

To see your requirements for uploading inventory to your retailers/channels, navigate to **Products** > **Product Feeds**

[ ](https://support.logicbroker.com/hs-fs/hubfs/Knowledge%20Base%20Import/Products_ProductFeeds_Main.png?hsLang=en)

First start by selecting your **Partner** (retailer/channel) at the top.

### Feed Specification

Clicking on the Feed Specification will show all the required fields and descriptions for the product content that needs to be uploaded.

[ ](https://support.logicbroker.com/hs-fs/hubfs/Knowledge%20Base%20Import/Products_ProductFeeds_FeedSpecification.png?hsLang=en)

Column | Description  
---|---  
**Field** |  Will include a friendly name used to describe the field.  
**Column Name** |  The exact column name that you will need to add in the CSV upload.  
**Required** |  Boolean field indicating if the field is required or optional.  
**Description** |  Full description on how the field is to be used, if there are conditional requirements, and the required options.  
  
If you click **Download Template** you can select a template that pertains to your specific product(s) **category**. If you select **All Categories** , all fields in the **Feed Specification** will be provided. Typically there will be different requirements for each category, therefore you can pick the template that best fits the products you are uploading.

[ ](https://support.logicbroker.com/hs-fs/hubfs/Knowledge%20Base%20Import/Products_ProductFeeds_FeedSpecification_DownloadTemplate.png?hsLang=en)

### Feeds

Once you upload your products you will see your results under **Feeds**. For every upload a unique **Feed ID** will automatically generate for each file. The file will process and show the number of **Items** and the number of **Compliant** items. **Compliant** means items that meets the required specification for the product being uploaded. If all items are compliant you will have the ability to **Send** the file to your retailer/channel; to do this click **Send** next to your feed.

[ ](https://support.logicbroker.com/hs-fs/hubfs/Knowledge%20Base%20Import/Products_ProductFeeds_Feeds.png?hsLang=en)

If you have **Non-Compliant** items, you can review and update your items by clicking **View** next to your feed. This will show a list of all your items and can be filtered to show all non-compliant items.

[ ](https://support.logicbroker.com/hs-fs/hubfs/Knowledge%20Base%20Import/Products_ProductFeeds_Feeds_View.png?hsLang=en)

By clicking on your product, you can edit specific fields. All missing data and **non-compliant** fields will be highlighted. Fields with multiple options, will include a drop down for all available options. Once all items are updated to be **compliant** , you can send the feed to your **retailer/channel;** clicking **SEND** will process the feed.

[ ](https://support.logicbroker.com/hs-fs/hubfs/Knowledge%20Base%20Import/Products_ProductFeeds_Feeds_View_Detail.png?hsLang=en)

### Events

All feeds **uploaded** and **exported** (sent) will generate an **event**. Feeds uploaded you will see **Product Feed Imported**. For import errors you will see **Product Import Error** ; this will usually indicate the file did not parse correctly and cannot be viewed under **Feeds**. Click **View** next to the event to review the details; usually this is due to not providing the data in the correct format. For all feeds sent to your **retailer/channel** , you will see an event logged **Product Feed Exported**.

[ ](https://support.logicbroker.com/hs-fs/hubfs/Knowledge%20Base%20Import/Products_ProductFeeds_Events.png?hsLang=en)

### Setting Up an Integration

To automatically send your product content feeds to your channel/retailer; there are 2 options using an **SFTP/FTP** connection or **API**.

For SFTP/FTP you can login to your Logicbroker SFTP/FTP directories by using your normal portal login and navigating to **/Product/Outbound** to upload your CSV in the required retailer/channel's format.

#### __ 🗒️Note:

Once the file is uploaded, you will still need to **login** in the portal ( **Products** > **Product Feeds**) to review, **fix** non-compliant products, and **send** the file to the retailer/channel.

For **API** integrations you can follow the steps in our [developer documentation](https://dev.logicbroker.com/#bb4a2e44-6b71-dec8-f4be-8c34e1e07d00).

####  ✨Tip:

Logicbroker can also support custom formats and integrations to your system. [Contact us](mailto:sales@logicbroker.com) for more details on setting this up to your system.