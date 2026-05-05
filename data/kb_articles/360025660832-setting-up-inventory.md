---
title: "Setting Up Inventory"
url: "https://support.logicbroker.com/kb/logicbroker/360025660832-setting-up-inventory"
category: "Retailer Onboarding"
---

March 10, 2026

# Setting Up Inventory

## 

The first step in getting setup in the Logicbroker Portal involves setting up your products for inventory transmission to your channel/retailer. 

#### ✨Tip:

Not all retailers/channels are capable of receiving inventory feeds. It is best to always check with your partner to verify their requirements.

#####   
Matching File

#### ✨Tip:

IMPORTANT: Not all users are required to load a matching file. Before starting the matching file process, confirm with Logicbroker Support whether the retailer or supplier should be loading the matching file. 

Select the **Partner** you plan to set up inventory for: 

##### 

Sending an inventory update to your partner will first involve setting up a link between your **SupplierSKU** and the **MerchantSKU**. Creating this link for each item will allow you to send inventory updates with only the **SupplierSKU** and will automatically match and update the quantity for that product and retain the **MerchantSKU** , even if it wasn't provided in the update. 

This is done to prevent sending products that are not set up in the Channel/Retailer's system. In this way, the process is separated so that any new products available to be updated via Inventory Feed will need to be setup using this **matching file** first. This will allow you to send all products in your inventory updates and the only products that will update are ones that have been set up previously. 

You can also view a list of your unmatched products by going to **Download Files** and downloading the **Unmatched Items** CSV or XLSX. If **Ignore unmatched** under Feed Settings is set, no unmatched records will be kept.

#### ✨Tip:

To avoid the process of setting up products with a matching file, you may be able to set the **Auto match** option under **Feed Settings**. If you aren't sure, confirm with Logicbroker Support. **Auto match** will allow you to submit all inventory feeds using your standard item feed, and any products will automatically get created with a **MerchantSKU** that matches the **SupplierSKU** provided. This should be used in cases where the **MerchantSKU** is the same as the **SupplierSKU,** or it is not required to provide the **MerchantSKU** or it is provided in another field.

Setting up your matching file begins by downloading the Standard Feed and populating the **MerchantSKU** and **SupplierSKU** fields. No other data will update when submitting the matching file.

##### 

[](https://support.logicbroker.com/hubfs/Knowledge%20Base%20Import/MatchingFileExample.png?hsLang=en)

Once your prepared your file, you can upload it and select **Matching File.**

##### 

##### Uploading Inventory

Now that you have set up your products, you can begin updating the inventory and other attributes for those items. Begin by downloading the **Standard Feed** under the **Download Files** section. You can download CSV or XLSX. 

For all the products listed in that file, you can begin adding attributes such as Quantity, Description, Cost etc. For more details on all the field attributes and the standard, see the [Inventory Specification](/kb/logicbroker/360022025472-Inventory-Specification?hsLang=en) under the **Document Standards** section.

When uploading the new file make sure **Standard Feed** is selected.

#### ✨Tip:

If you have a customer inventory CSV or XLSX mapped to our standard you can use the **Supplier Feed**. To learn more about setting up a custom CSV or XLSX format [contact support](mailto:support@logicbroker.com).

Once your feed is uploaded, we validate the format for that partner. We only check to verify all proper fields are populated for the partner selected, we do not do any validation to verify the SKUs match in the partner's system.

After the processing is complete you will see an audit log of all inventory uploaded attempts under **Events**. Here you can view all transmissions and review any errors from failed submissions.

##### 

Based on the partner you are integrating with Logicbroker will send the inventory update on a periodic basis. This differs between channels/retailers, but typically will send at least once every 24 hours. The inventory feed will only send updated products from the last transmission to the retailer. 

For example, if you had 100 products setup, and sent 2 feeds, one updating 25 and 50 in the other; the next update sent to your partner will show 75 products in the inventory update.

#### ✨Tip:

If you send multiple feeds before the update is transmitted to your partner, and only want to include information from the last feed, you can enable **Latest Feed Only** under feed settings.

For more information on other settings available on the **Inventory Feeds** page see information below.

**Feed Settings**

Under the Feed Settings section there are a few things you can setup to help you process files. 

**Clear After**

This will allow you to clear your inventory after the selected time. We allow periods of 7, 30 and 60 days. This will remove all your items based on the period selected requiring you to setup new items after all items have cleared. This should always be used to maintain an up to date list of products.

* * *

**Allocation**

If you are sending the same inventory counts across all your partners, you can setup an allocation percentage under each partner. If you select 50%, and submit an inventory count for an item of 20, the update sent to your partner will be 10. This allocation will be done by for all products within the inventory feed.

* * *

**Auto match**

This will allow you to submit all inventory feeds using your standard feed and any products not matched will automatically get created with the MerchantSKU matching the SupplierSKU provided. This should be used in cases where the MerchantSKU is the same as the SupplierSKU, it is not required to provide the MerchantSKU or provided in another field. The MerchantSKU can only be set to a different value then the SupplierSKU through the matching file.

* * *

**Case-sensitive**

When submitting inventory feeds, all updates depend on matching the SupplierSKU. If you do not want your SupplierSKUs to match when the case doesn't match, then select this option.

* * *

**Ignore unmatched**

If this option is checked and items are sent that aren't matched they will not show up in the **unmatched items** report in the Download Files section.

* * *

**Latest feed only**

If you send multiple feeds before an update is transmitted to your partner, and only want to include information from the last feed select this option. For example, if you send 2 feeds, one with 20 items and another with 10, the update sent to your partner will only include the 10 with this option selected.

**Clear Feeds**

**Remove All Items**

Selecting this will remove **all** item information setup for your partner.

* * *

**Clear All SKU Matches**

Selecting this will remove the **MerchantSKU** for all items setup. All other information will be retained and will allow you to setup new MerchantSKUs on those items. Use this if incorrect MerchantSKUs were setup on your items, but you want to retain all other item information already setup. 

**Download Files**

**Merchant Feed**

This is the format your partner has setup, this can be a custom CSV or XLSX template, but typically will be the same as the Standard Feed.

* * *

**Standard Feed**

This is the standard inventory specification containing all available item attributes. For more information on these attributes see the [Inventory Specification](/kb/logicbroker/360022025472-Inventory-Specification?hsLang=en) page.

* * *

**Unmatched Items**

This will contain all items that were sent in your inventory updates that did not have a matching **SupplierSKU**. If **Auto match** is setup, no unmatched items will appear in this list.

##### 

##### Automating the Process

To automate the process of setting up products for inventory there are 2 options. You can integrate using **SFTP/FTP** or through the **API**. In both scenarios, the format will be the same using a standard **CSV** or **XLSX** file with the columns **SupplierSKU** and **MerchantSKU**.

For **SFTP/FTP** you can connect by following the [instructions](/kb/logicbroker/360022067631-SFTP-FTP?hsLang=en) here. Once connected you will need to upload the matching file to the following directory -

**/ManagedInventory/ <PartnerAccount>/OutboundMatching**

**The <PartnerAccount> will be your supplier's **Company ID**. This can be retrieved by navigating to [Suppliers](https://stageportal.logicbroker.com/scorecards) in the portal; the **CompanyID** will be shown under each supplier.

To integrate using the **API** please follow [these instructions](https://dev.logicbroker.com/#c05bc45b-6f93-c4f5-8fec-e386876c0754) in the **Retailer Inventory** section on our developer site.

##### Vendor Sourcing

The Matching file is also used to source orders to the correct vendor (when sourcing by SKU). When a sales order is being processed, the matching file is used to identify which vendor each line will be sourced to, based on product. If a product is encountered that has not be setup for a specific vendor (the product does not appear on any matching file), the order will not be able to complete the sourcing process. This allows time for a match to be added, and the sales order reprocessed.