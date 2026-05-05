---
title: "Step 5: Setup Notifications and Monitoring Alerts"
url: "https://support.logicbroker.com/kb/logicbroker/360022057611-step-5-setup-notifications-and-monitoring-alerts"
category: "Supplier Onboarding"
---

March 12, 2026

# Step 5: Setup Notifications and Monitoring Alerts

## 

[🔗(STAGE) New order summary.htm](https://support.logicbroker.com/hubfs/logicbroker_media/\(STAGE\)%20New%20order%20summary.htm?hsLang=en) (90 KB)  
---  
[🔗(STAGE) New invoice summary.htm](https://support.logicbroker.com/hubfs/logicbroker_media/\(STAGE\)%20New%20invoice%20summary.htm?hsLang=en) (90 KB)  
[🔗(STAGE) New shipment summary.htm](https://support.logicbroker.com/hubfs/logicbroker_media/\(STAGE\)%20New%20shipment%20summary.htm?hsLang=en) (90 KB)  
[🔗(STAGE) New return summary.htm](https://support.logicbroker.com/hubfs/logicbroker_media/\(STAGE\)%20New%20return%20summary.htm?hsLang=en) (90 KB)  
  
Notifications and Monitoring alerts are emails that are triggered to your configured address to proactively monitor your system. Reports can be configured to have alerts sent when errors occur, or when encountering connectivity issues. Navigate to **Settings** > **Notification Configuration** to setup your subscriptions. This will help manage your integrations with all retailers/channels to ensure you are always sending/receiving compliant data.

[Stage Notification Link](https://stageportal.logicbroker.com/profile/notifications)

[Production Notification Link](https://portal.logicbroker.com/profile/notifications)

Notification Descriptions 

Listed below is all the available information, errors, and monitoring alerts that can be configured. By default some notifications are automatically subscribed to your account. See the **default** check mark next to the notification. Click the notification to view a sample of the email notification that you will receive when triggered.

_**Please note**_ : Default notifications are only configured in production. Stage notifications will need to be turned on manually.

#### ✨Tip:

You can include additional default notifications for all users added to your company. If you would like additional subscriptions defaulted automatically for your user [contact support](mailto:support@logicbroker.com).

**Information**

Notification | Description | Default  
---|---|---  
[**New order**](https://support.logicbroker.com/hubfs/logicbroker_media/\(STAGE\)%20New%20order%20summary.htm?hsLang=en) |  Provides a count of all new orders received in the past hour. Will include a link to view the new orders in the Portal.  |   
[**New shipment**](https://support.logicbroker.com/hubfs/logicbroker_media/\(STAGE\)%20New%20shipment%20summary.htm?hsLang=en) |  Provides a count of all new shipments received in the past hour. Will include a link to view the new shipments in the Portal.  |   
[**New invoice**](https://support.logicbroker.com/hubfs/logicbroker_media/\(STAGE\)%20New%20invoice%20summary.htm?hsLang=en) |  Provides a count of all new invoices received in the past hour. Will include a link to view the new invoices in the Portal. |   
[**New return**](https://support.logicbroker.com/hubfs/logicbroker_media/\(STAGE\)%20New%20return%20summary.htm?hsLang=en) |  Provides a count of all new returns received in the past hour. Will include a link to view the new returns in the Portal.  |   
[**Order cancellation**](https://support.logicbroker.com/hubfs/logicbroker_media/SupplierCo-RetailerCo%20Order%20%23PO1739141-001%20Cancelled.htm?hsLang=en) |  Triggered when an order is cancelled. |  ✅  
**Monitoring alert** |  Enables monitoring reports with thresholds configured under the Monitoring page. To learn more about monitoring configurations, see the monitoring section below. |  ✅  
[**Daily activity summary**](https://support.logicbroker.com/hubfs/logicbroker_media/Daily%20Activity%20Summary.htm?hsLang=en) |  Will provide a daily a list daily of total documents transmitted through the system, with a breakdown of Total Orders, Open Orders, Complete Orders, Total Shipments and Total Invoices. This can be configured in the Monitoring section, no parameters are required for configuration. |   
[**Monthly document count**](https://support.logicbroker.com/hubfs/logicbroker_media/Monthly%20Document%20Report.htm?hsLang=en) |  Will send once a month including all information breakdown of all documents sent in that month. This includes # of orders, shipments and invoices. Must setup the **Monthly Document Report** under Monitoring to receive email notification. |   
[**Monthly order count**](https://support.logicbroker.com/hubfs/logicbroker_media/Monthly%20Order%20Report.htm?hsLang=en) |  Will send once a month and include the total number of orders received for that month. Must setup the **Monthly Order Report** under Monitoring to receive email notification. |   
[**FTP activity (file upload/delete)**](https://support.logicbroker.com/hubfs/logicbroker_media/FTP%20Activity.htm?hsLang=en) |  Logicbroker monitors all SFTP/FTP activity on the hosted platform. If a user uploads, deletes or edits a document on the SFTP/FTP server, the username, company id, IP address and directory the action took place in will be logged in the email. This is to track when users are logging in and verify when files are downloaded. |   
[**Unknown EDI documents**](https://support.logicbroker.com/hubfs/logicbroker_media/STAGE%20Unable%20to%20determine%20senderreceiver%20for%20EDI%20846%20%23100001857-2.htm?hsLang=en) |  Will trigger when an EDI document is received for your account and your partner's identifiers do not match any partners you are connected to. |  ✅  
[**Failed document report**](https://support.logicbroker.com/hubfs/logicbroker_media/Failed%20Shipments.htm?hsLang=en) |  Need to configure under the Monitoring to setup a full list of all documents that are in a Failed status within the system. This includes Orders, Acknowledgements, Shipments, and Invoices. |  ✅  
[**Inventory update report**](https://support.logicbroker.com/hubfs/logicbroker_media/Inventory%20Update%20Report.htm?hsLang=en) |  Need to configure under the Monitoring page. Subscribing will provide an inventory update summary for all your partners once every 24 hours. It will include Total Items, Total Updates, Matched Items, Matched Updates, Unmatched Items and In Stock % for each partner. |  ✅  
[**Unmatched inventory report**](https://support.logicbroker.com/hubfs/logicbroker_media/Unmatched%20Inventory%20Report.htm?hsLang=en) |  Need to configure under the monitoring page. Will provide an update every 24 hours with all partners unmatched items count. |  ✅  
[**Inventory activity**](https://support.logicbroker.com/hubfs/logicbroker_media/Inventory%20Imported%20for%20Supplier%20Co.htm?hsLang=en) |  Will provide an update every time inventory is uploaded by one of your partners. This will include number of items and the link to the file uploaded to download. |   
[**Document aging report**](https://support.logicbroker.com/hubfs/logicbroker_media/Retailer%20Co%20Order%20Aging%20Report.htm?hsLang=en) |  Will need to configure under the monitoring page. Will provide a full list of all partners and order counts for all documents not complete with their aging. Ranges include < 7 days, 7-14 days, 14-30 days, 30-60 days, and >60 days. The report can be configured to run daily at midnight or morning. |  ✅  
[**Trading partner notification**](https://support.logicbroker.com/hubfs/logicbroker_media/Notification%20From%20Retailer%20Co%20To%20Supplier%20Co.htm?hsLang=en) |  Email will be sent when a trading partner sends a message. The message can be sent through the messaging center or through EDI like an 864 text message. In addition, if a document is received that does not map to a standard Logicbroker Document Type (Order, Acknowledgement, Shipment, Invoice, Return or Inventory) a notification will be sent with details as well. |  ✅  
[**Score card**](https://support.logicbroker.com/hubfs/logicbroker_media/Supplier%20Score%20Cards.htm?hsLang=en) |  Will provide a weekly score card for all your partners. This will include overall score, shipment time, shipment % and cancel %. |   
[**Routing instructions**](https://support.logicbroker.com/hubfs/logicbroker_media/Routing%20Instructions%20for%20Shipment%20%2319427964.htm?hsLang=en) |  Available if using routing instructions (for EDI this is the 754) with your channel/retailer. Notification will provide reference numbers, shipment pickup time, carrier, and carrier contact information. |   
[**GDPR notification**](https://support.logicbroker.com/hubfs/logicbroker_media/GDPR%20Redaction%20Report.htm?hsLang=en) |  Will provide an update of all redacted documents related to your account. |   
[**Testing completed**](https://support.logicbroker.com/hubfs/logicbroker_media/Testing%20Complete%20for%20Visionary%20Sleep%20LLC.htm?hsLang=en) |  Will provide an update when testing has been completed for your partner. |   
  
**Errors**

Notification | Description | Default  
---|---|---  
[**SKU not found**](https://support.logicbroker.com/hubfs/logicbroker_media/SKU%20not%20found.htm?hsLang=en) |  Used if connected to a system and a SKU couldn’t be found when inserting a document into your system. |  ✅  
[**Order sourcing failed**](https://support.logicbroker.com/hubfs/logicbroker_media/Drop%20Ship%20Sourcing%20Error%20for%20Retailer%20Company.htm?hsLang=en) |  Used if using Logicbroker's purchase order routing logic. Occurs when a supplier can not be found to create a purchase order off of a sales order received. |  ✅  
[**Business rule failed**](https://support.logicbroker.com/hubfs/logicbroker_media/Shipment%20%23231848%20Failed.htm?hsLang=en) |  Triggered if a business rule fails to run, this will typically contain complex validation logic for all documents sent or received. |   
[**Failed to update shipping information**](https://support.logicbroker.com/hubfs/logicbroker_media/Failure%20to%20Update%20Tracking%20Information.htm?hsLang=en) |  Sent when shipments failed to update on the order. This occurs when items do not match the original order. |   
[**Tracking upload failed**](https://support.logicbroker.com/hubfs/logicbroker_media/Tracking%20Upload%20Failed.htm?hsLang=en) |  Triggered when an a bulk CSV/XLSX upload is made in the portal (under Order Management) and the upload fails. Will provide detailed information for the failure reason. |  ✅  
[**External XML translation alert**](https://support.logicbroker.com/hubfs/logicbroker_media/File%20Translation%20Error.htm?hsLang=en) |  Triggered if you are using a custom XML format and translation fails to create the document inside the Logicbroker system. |   
[**Inventory error**](https://support.logicbroker.com/hubfs/logicbroker_media/Failed%20Inventory%20Import.htm?hsLang=en) |  Will provide an email if you or your partner attempted to process and inventory update and it failed. Notification will provide a link to download the file and details on why the update failed. |  ✅  
[**API error**](https://support.logicbroker.com/hubfs/logicbroker_media/API%20Communication%20Failed.htm?hsLang=en) |  Triggered if you are integrating using an API connection to a system and Logicbroker fails to connect to that system. |   
[**Scheduled task failed**](https://support.logicbroker.com/hubfs/logicbroker_media/Scheduled%20Task%20Failed%20for%20Bed%20Bath%20and%20Beyond.htm?hsLang=en) |  Triggered if there is a scheduled job setup on your account and fails to process. This can include a job scheduled to pick up files from an external SFTP/FTP site or sending data to a configured connection; for example sending inventory updates on a schedule. |   
[**Document validation failed**](https://support.logicbroker.com/hubfs/logicbroker_media/Document%20%2319607853%20Failed%20Validation.htm?hsLang=en) |  Triggered when a document either sent or received fails validation from wither you or your partners requirements. Full details will be provided in the email. |   
  
**Warnings**

Notification | Description | Default  
---|---|---  
[**Login to external system failed**](https://support.logicbroker.com/hubfs/logicbroker_media/Login%20Failure.htm?hsLang=en) |  Triggered if you are connected to a system using a pre-built connector and Logicbroker receives a connection error. The connection will continue to retry, however the warning is sent with full details for visibility to potential issues. |   
[**Overdue acknowledgments**](https://support.logicbroker.com/hubfs/logicbroker_media/Orders%20Overdue%20for%20Acknowledgment.htm?hsLang=en) |  Will provide a list of all orders that are awaiting functional acknowledgements (997), this is set to orders that haven't been acknowledged over 24 hours. |  ✅  
[**Overdue documents**](https://support.logicbroker.com/hubfs/logicbroker_media/Orders%20Overdue.htm?hsLang=en) |  Configured under the Monitoring page. Will provide a list of documents that are still open (any status less than 1000). Similar to the aging report however will provide a list of open orders, with a maximum of 50 in each report. *Note: for Orders, this report will not take into account the **Requested ship date.** |  ✅  
[**Overdue inventory**](https://support.logicbroker.com/hubfs/logicbroker_media/Overdue%20Inventory%20Report.htm?hsLang=en) |  Provides a list of all partners who haven't provided inventory in over 24 hours. Total Items, Matched Items and Unmatched Items are also provided. |  ✅  
  
**Monitoring**

To setup your custom monitoring reports, go to **Settings** > **Monitoring**. For all configurations that use a threshold, you will need to make sure **Monitoring Alert** is subscribed to under **Notification Configurations** ; this will enable receiving emails for the configured reports.

[Stage Monitoring Link](https://stageportal.logicbroker.com/settings/monitoring)

[Production Monitoring Link](https://portal.logicbroker.com/settings/monitoring)

Notification | Description | Default  
---|---|---  
[**Document Aging Report**](https://support.logicbroker.com/hubfs/logicbroker_media/Retailer%20Co%20Order%20Aging%20Report.htm?hsLang=en) |  Will provide a full list of all partners and order counts for all documents not complete with their aging. Ranges include < 7 days, 7-14 days, 14-30 days, 30-60 days, and >60 days. |   
[**Document Aging Report (Midnight)**](https://support.logicbroker.com/hubfs/logicbroker_media/Retailer%20Co%20Order%20Aging%20Report.htm?hsLang=en) |  Same as Document Aging Report except runs daily at midnight. |   
[**Document Aging Report (Morning)**](https://support.logicbroker.com/hubfs/logicbroker_media/Retailer%20Co%20Order%20Aging%20Report.htm?hsLang=en) |  Same as Document Aging Report except runs daily at 9:30AM EST. |   
[**Documents Stuck in Submitted ( >1h)**](https://support.logicbroker.com/hubfs/logicbroker_media/Orders%20Overdue.htm?hsLang=en) |  Lists all documents that remain in the Submitted status for over 1 hour. Typically indicates the documents have not been picked up by you or your partner's system yet and could indicate a potential issue. |   
[**Failed Document Report (24h)**](https://support.logicbroker.com/hubfs/logicbroker_media/Failed%20Shipments.htm?hsLang=en) |  Provides a full list of all documents that are in a Failed status within the system. Can be configured for Orders, Acknowledgements, Shipments, and Invoices. |   
[**Failed Documents (24h) (Midnight)**](https://support.logicbroker.com/hubfs/logicbroker_media/Failed%20Shipments.htm?hsLang=en) |  Same as Failed Document Report, however the report will run at midnight. |   
[**Hourly Failed Documents**](https://support.logicbroker.com/hubfs/logicbroker_media/Failed%20Shipments.htm?hsLang=en) |  Provides a report of all failed documents hourly. |   
[**Inventory Update Report**](https://support.logicbroker.com/hubfs/logicbroker_media/Inventory%20Update%20Report.htm?hsLang=en) |  Will provide an inventory update summary for all your partners once every 24 hours. It will include Total Items, Total Updates, Matched Items, Matched Updates, Unmatched Items and In Stock % for each partner. |   
[**Monthly Document Report**](https://support.logicbroker.com/hubfs/logicbroker_media/Monthly%20Document%20Report.htm?hsLang=en) |  Provides a summary of all documents processed for the month. Includes a count for orders, acknowledgements, shipments and invoices. |   
[**Monthly Order Report**](https://support.logicbroker.com/hubfs/logicbroker_media/Monthly%20Order%20Report.htm?hsLang=en) |  Provides a summary count of all orders processed for the month. |   
[**New Document Activity (24h)**](https://support.logicbroker.com/hubfs/logicbroker_media/Daily%20Activity%20Summary.htm?hsLang=en) |  Monitors how often you expect documents to be received in your system. For example if you expected minimum of orders received is 400, then you can set the threshold to 400 and the report will get triggered when the # of order received is below that 400 threshold. |   
[**New Document Activity (24h) (Midnight)**](https://support.logicbroker.com/hubfs/logicbroker_media/Daily%20Activity%20Summary.htm?hsLang=en) |  Same as above, however will run at midnight. |   
[**Order 72 Hours Overdue to Ship**](https://support.logicbroker.com/hubfs/logicbroker_media/Orders%20Overdue.htm?hsLang=en) |  Lists all orders that have not shipped within 72 hours from the **Requested Ship Date**. A maximum of 50 orders will be listed. |   
[**Overdue Documents (24h) (Midnight)**](https://support.logicbroker.com/hubfs/logicbroker_media/Orders%20Overdue.htm?hsLang=en) |  Will provide a list of documents that are still open. Similar to the aging report; however, will provide a list of open orders, with a maximum of 50 in each report. |   
[**Overdue Documents (48h)**](https://support.logicbroker.com/hubfs/logicbroker_media/Orders%20Overdue.htm?hsLang=en) |  Same as above, however, will provide a list for all orders overdue after 48 hours. |   
[**Overdue FuncAcks (48h) (Midnight)**](https://support.logicbroker.com/hubfs/logicbroker_media/Failed%20Functional%20Ackowledgement.htm?hsLang=en) |  If you are communicating with your partner using EDI, all documents sent to your partner expect to receive a FuncAck (997), if one is not received in over 48 hours the report will include a the document. |   
[**Overdue FuncAcks (48h) (Morning)**](https://support.logicbroker.com/hubfs/logicbroker_media/Failed%20Functional%20Ackowledgement.htm?hsLang=en) |  Same as above, however, the report will run 9:30AM |   
[**Shipped Order Aging Report**](https://support.logicbroker.com/hubfs/logicbroker_media/Retailer%20Co%20Order%20Aging%20Report.htm?hsLang=en) |  Provides a full list of orders that have shipments applied to them, however, not all items have been fully shipped. |   
[**Unmatched Inventory Report**](https://support.logicbroker.com/hubfs/logicbroker_media/Unmatched%20Inventory%20Report.htm?hsLang=en) |  Will provide an update every 24 hours with all partners unmatched items count. Used only for retailers. |   
[**Weekly Supplier Scorecard**](https://support.logicbroker.com/hubfs/logicbroker_media/Supplier%20Score%20Cards.htm?hsLang=en) |  Provides a weekly summary of all partners score card information. This will include overall score, shipment time, shipment % and cancel %. Used only for retailers. |