---
title: "Document Statuses"
url: "https://support.logicbroker.com/kb/logicbroker/360022067771-document-statuses"
category: "Document Standards"
---

March 10, 2026

# Document Statuses

## 

For all documents processed through Logicbroker, statuses are used to track the automatic processing and actions needed to take. Workflows can be configured to fit how and when you need to receive your documents. Contact support for more information on customizing your flows.

The standard statuses listed below for each document show the standard statuses and normal processing we follow.

**Order**

Status ID | Status Name | Description  
---|---|---  
**0** |  **New** |  When a document is created in the Logicbroker sytem, all documents will process in the New status, eventually proceeding to **Submitted (100)**. Documents should not be updated or edited when in the **New (0)** status. Here configured rules and asynchronous data validation are run for the receiving partner. To re-send your document it is best practice to reset to **New (0)** for all necessary processing to run before re-sending.  
**100** |  **Submitted** |  If you are picking up your document via API or SFTP/FTP (JSON, XML, and CSV Only), you will see your document sit in this status. Once the document is processed it will automatically move to **Acknowledged (200)** to indicate the document was successfully picked up.  
**150** |  **Ready to Acknowledge** |  Status indicates the order is waiting for acknowledgement. In some cases if using API or SFTP/FTP integration, the process can be configured to pick up files in this status instead of **Submitted (100)**. This is done to add addition custom workflow configurations for you. This can be sending the document to another location before it is picked up or doing conditional routing.  
**200** |  **Acknowledged** |  Used to indicate that the Order was successfully picked up, and is ready to receive an Acknowledgement. Once an Acknowledgement is received the Order will automatically move to the **Ready to Ship (500)** status. If you have auto-acknowledge setup on your account, the acknowledgement will auto-create on this status and move to **Ready to Ship (500)** as well.  
**400** |  **Ready to Fulfill** |  Used for interim processing using customized flow. Normal users will not use this status. Contact support to learn how you can use statuses to customize your workflows.  
**500** |  **Ready to Ship** |  Status indicates the order is waiting for a Shipment. When the shipment is received and all items from the original order have been shipped, the status will move to **Ready to Invoice (600)** if the partner requires an invoice, if not the status will move to **Complete (1000)**.  
**530** |  **Shipped** |  Indicates that an order has been fully shipped. This status is used when the **Logicbroker Parcel Movement** feature is enabled. Status is updated when all item's shipment's tracking numbers are processed and shipped.  
**600** |  **Ready to Invoice** |  Status indicates the system is waiting for invoice. When the Invoice is received and all quantities from the original order have been invoiced the status of the order will move to **complete (1000)**.  
**1000** |  **Complete** |  Status indicates the order is complete and all items have been shipped and/or invoiced on the order.  
**1100** |  **Cancelled** |  Status indicates that all items are cancelled. This is done by sending related Acknowledgements for your order and marking all the ordered quantities as cancelled. If line items have been partially cancelled the order will not move to this status.  
**1200** |  **Failed** |  Status indicates the document failed to process to the partner. To review the error, view the events associated with the document. This can be viewed through API or through the portal under events.  
**1400** |  **Ignored** |  Status indicates that the document should be ignored and not fulfilled. Used when resending a document that has failed. You should mark the original as ignored and retranmsit a new version. Documents will also automatically move to **Ignored (1400)** if it's been in a **Failed (1200)** status for longer then 30 days.  
  
**Acknowledgement**

Status ID | Status Name | Description  
---|---|---  
**0** |  **New** |  When a document is created in the Logicbroker sytem, all documents will process in the New status, eventually proceeding to **Submitted (100)**. Documents should not be updated or edited when in the **New (0)** status. Here configured rules and asynchronous data validation are run for the receiving partner. To re-send your document it is best practice to reset to **New (0)** for all necessary processing to run before re-sending.  
**100** |  **Submitted** |  If you are picking up your document via API or SFTP/FTP (JSON, XML, and CSV Only), you will see your document sit in this status. Once the document is processed it will automatically move to **Acknowledged (200)** to indicate the document was successfully picked up.  
**200** |  **Processing** |  Internal status indicating that Logicbroker is processing the document to be sent to partner. No action is required on this status.  
**1000** |  **Complete** |  Document has been successfully transmitted to partner.  
**1200** |  **Failed** |  Status indicates the document failed to process to the partner. To review the error, view the events associated with the document. This can be viewed through API or through the portal under the document detail.  
**1400** |  **Ignored** |  Status indicates that the document should be ignored and not fulfilled. Used when resending a document that has failed. You should mark the original as ignored and retranmsit a new version. Documents will also automatically move to **Ignored (1400)** if it's been in a **Failed (1200)** status for longer then 30 days.  
  
**Shipment**

Status ID | Status Name | Description  
---|---|---  
**0** |  **New** |  Business rule to format data properly. The status will automatically move to **Submitted (100)**.  
**-1** |  **Draft** |  Status will be used to download labels and edit the shipment before sending the document to the partner.  
**100** |  **Submitted** |  Status indicating that the document is ready to be sent to partner. The partner can receive the document by downloading to through VFTP or API. If picking up through API, status should be moved to **Processing (200)**. The document will automatically be moved to **Complete (1000)** status after updating the originating order.  
**200** |  **Processing** |  Internal status indicating that Logicbroker is processing the document to be sent to partner. Your original order will also get updated with quantity shipped and update the order status accordingly as well. No action is required on this status.  
**300** |  **Consolidating** |  Internal status indicating that Logicbroker is consolidating the shipment. No action is required on this status.  
**410** |  **Awaiting 754** |  **Only used when retailer is using the Routing Request (753) and Routing Instructions (754) documents. Indicates that the 753 Routing Request was sent to the retailer and waiting for a response with the instructions required to pick up the shipment. No action is required on this status.  
**420** |  **754 Received** |  **Only used when retailer is using the Routing Request (753) and Routing Instructions (754) documents. Indicates that a 754 Routing Instructions was received, this will trigger a notification indicating the pickup time, location and carrier information. Once the shipment is picked up, the shipment document must be moved to status **With Carrier** (**430)** by the user.  
**430** |  **With Carrier** |  Used when processing routing requests (753) and routing instructions (754). After the routing request is sent, instructions are received, and the shipment is marked as picked up, the shipment will move to status 430 (With Carrier). In addition, the status will be used for parcel tracking. Using the tracking number Logicbroker checks with the carrier to update the status of the shipment. In this case, no status was provided from the carrier and will remain in this status until a new event is received.To learn more about using parcel movement tracking contact [support](mailto:support@logicbroker.com).  
**435** |  **Unable to Track** |  **Only used when parcel movement tracking has been enabled. To learn more about parcel movement tracking contact [support](mailto:support@logicbroker.com). Shipment is moved to this status when no information can be found from the carrier using the tracking number. If one package on the shipment is **Unable to Track,** even if another package is in a further status, the shipment will remain in **Unable to Track**.  
**440** |  **Accepted** |  **Only used when parcel movement tracking has been enabled. To learn more about parcel movement tracking contact [support](mailto:support@logicbroker.com). Indicates the shipment label has been printed, but not yet picked up by the carrier. If one package is in the **Accepted** status and no status is less than **440 (Accepted)** , the entire shipment will remain in that status.  
**450** |  **In Transit** |  **Only used when parcel movement tracking has been enabled. To learn more about parcel movement tracking contact [support](mailto:support@logicbroker.com). Indicates the carrier has picked up the shipment. If one package is in the **In Transit** status and no status is less than **450 (In Transit),** the entire shipment will remain in that status.   
**460** |  **Delivery Attempted** |  **Only used when parcel movement tracking has been enabled. To learn more about parcel movement tracking contact [support](mailto:support@logicbroker.com). Indicates the carrier has attempted to deliver the shipment to the customer. If one package is in the **Delivery Attempted** status and no status is less than **460 (Delivery Attempted),** the entire shipment will remain in that status.   
**465** |  **Exception** |  **Only used when parcel movement tracking has been enabled. To learn more about parcel movement tracking contact [support](mailto:support@logicbroker.com). Indicates there was an error with the shipment/delivery; this can be any issue such as return to sender. If one package is in the **Exception** status, the entire shipment will remain in that status.   
**470** |  **Delivered** |  **Only used when parcel movement tracking has been enabled. To learn more about parcel movement tracking contact [support](mailto:support@logicbroker.com). Indicates the shipment was delivered to the end customer. The status will only be moved to **Delivered** if all items have been shipped and all packages are in the **Delivered** status.  
**1000** |  **Complete** |  Document has been successfully transmitted to partner.  
**1200** |  **Failed** |  Status indicates the document failed to process to the partner. To review the error, view the events associated with the document. This can be viewed through API or through the portal under the document detail.  
**1400** |  **Ignored** |  Status indicates that the document should be ignored and not fulfilled. Used when re-sending a document that has failed. You should mark the original as ignored and re-transmit a new version. Documents will also automatically move to **Ignored (1400)** if it's been in a **Failed (1200)** status for longer then 30 days.  
  
**Invoice**

Status ID | Status Name | Description  
---|---|---  
**0** |  **New** |  Business rule to format data properly. The status will automatically move to **Submitted (100)**.  
**100** |  **Submitted** |  Status indicating that the document is ready to be sent to partner. The partner can receive the document by downloading to through VFTP or API. If picking up through API, status should be moved to **Processing (200)**. The document will automatically be moved to **Complete (1000)** status after updating the originating order.  
**110** |  **Consolidated** |  Status indicating that the invoice has been consolidated.  
**200** |  **Processing** |  Internal status indicating that Logicbroker is processing the document to be sent to partner. Your original order will also get updated with quantity invoiced and update the order status accordingly as well. No action is required on this status.  
**1000** |  **Complete** |  Document has been successfully transmitted to partner.  
**1200** |  **Failed** |  Status indicates the document failed to process to the partner. To review the error, view the events associated with the document. This can be viewed through API or through the portal under the document detail.  
**1400** |  **Ignored** |  Status indicates that the document should be ignored and not fulfilled. Used when resending a document that has failed. You should mark the original as ignored and retranmsit a new version. Documents will also automatically move to **Ignored (1400)** if it's been in a **Failed (1200)** status for longer then 30 days.