---
title: "Product/Inventory FAQs"
url: "https://support.logicbroker.com/kb/logicbroker/7908242820500-product-inventory-faqs"
category: "Platform"
---

March 13, 2026

# Product/Inventory FAQs

## 

Below you will find the most frequently asked questions for product and inventory, please click on the headings below to be directed to the specific section. 

  * Product Feeds
  * Inventory



### **Product Feeds**

**Can you map to my taxonomy?**

_*Only applicable to retailers_

_Yes, using custom attributes._

**Can you send the data directly to my PIM?**

_*Only applicable to retailers_

_No, you must extract the information out of Logicbroker’s Portal via API, CSV, or FTP and import it into your PIM._

**Can I use my own categories?**

_Categories are established based on retailer requirements. These can be viewed in the Feed Specification section on the Product Feeds Page._

**Can I upload videos?**

_Yes, video links are supported in Product Feeds. These links should not be password protected._

**Are there image/video size requirements?**

_No, there are no size requirements for media when uploading to Product Feeds._

**Can I upload DOC's or certificates as a PDF?**   
_Yes, PDF and DOC links are supported in Product Feeds._

**Can I help my vendors onboard their feeds?**

_*Only applicable to retailers_

_Yes, you can download the CSV file and review errors to help troubleshoot._

**Can I add subcategories?**

_Yes. To add a subcategory, add a column to the file and name it subcategory. You are then able to populate the information and upload the file._

**Do I get notified when suppliers upload feeds?**

_Yes. There is a notification type retailers can subscribe to under Settings > Notifications called “Product Feeds Notification”._

**Can I add additional attributes at a later date?**

_Yes, suppliers can always go back to add additional attributes and re-upload the files to strengthen their products._

### **Inventory**

**Do I have to use the Logicbroker Inventory Template?**

_*Only applicable to suppliers manually uploading inventory to Logicbroker using Excel/CSV_

_Yes, this template is pre-mapped into our system and will ensure the quickest and most effective upload - using a different template will cause issues._

**Why are leading zeroes being deleted from my feed?**

_*Only applicable to suppliers manually uploading inventory to Logicbroker using Excel/CSV_

_If you have item values with leading zeroes, Excel will automatically remove them. To fix this, you can either:_

  1. _change the column to**Text** format instead of**General** or **Number** Format _
  2. _add an**apostrophe** to the begging of your input (ex.**'** 00548663) - this will keep all your formatting in place_



**Why are my items showing up in scientific notation?**

_*Only applicable to suppliers manually uploading inventory to Logicbroker using Excel/CSV_

_SKUs and UPCs are often reverted to scientific notation due to their long number sequence.__To fix this, you can_ _change the column that shows up in scientific notation to a**Text** format instead of a **General** or **Number** format._

**Do I need to have inventory in the portal before completing test cases?**

_*Only applicable to suppliers processing test cases in Logicbroker_

_Yes, all suppliers need to have inventory in the stage portal before moving on to test cases since test cases are generated using items from your inventory feed._

**I sent my 846 but it is not showing up in the stage portal?**

_*Only applicable to EDI suppliers_

_Make sure you are using the correct stage/test AS2 Identifier:**STAGELOGICBROKERAS2** , confirm you have our **[Connection Information](http://help.logicbroker.com/hc/en-us/sections/360003409311-Connection-Information?hsLang=en)** set up correctly and that your EDI connection is working._

**Why is there an error in my inventory upload?**

_If you upload your inventory and see the error:**Inventory Import Error** under the **Events** log, click on **View** to download a full report on why your inventory failed. Troubleshoot/adjust your feed from the feedback in this report and reupload/resend a new file. _

**How do I know if my upload worked?**

_Once you upload your inventory as a**Standard Feed** , you should see it under **Events**. The **Events** log will show you the time stamp of your upload, the summary (should say: **Inventory Imported**) and the user (if it was a manual upload). To see a copy of the upload, click on **View**. If there were any errors in your upload, the **Summary** will say **Inventory Import Error**._