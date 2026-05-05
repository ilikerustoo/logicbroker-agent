---
title: "Failed Document Summary"
url: "https://support.logicbroker.com/kb/logicbroker/14011075132692-failed-document-summary"
category: "Platform"
---

March 5, 2026

# Failed Document Summary

## 

**Audience:** All users in Logicbroker.

In this article, you will find information related to the Failed Document Summary to understand better how it works. The sections within this article are outlined below:

  * Overview
  * Navigating the Summary
  * Extracting the Data from Logicbroker

Overview

Logicbroker offers the Failed Document Summary on the platform to all users. This report is used to manage document failures, by document type or failure reason, and troubleshoot accordingly. To access this feature, navigate to the**left-hand side toolbar** and click on **Reports** and select **Failed Documents** from the dropdown.

Navigating the Summary

To better understand the Failed Document Summary, we will look at terminology and some common failures seen in this report. The terminology (shown in the "At a Glance" tab) will help users better understand what each column of the report is referring to. The common failures (shown in the "Failure Types" tab) will help users understand why the document failed and what can be done to fix the failure issue.

**At a Glance**

**Sender **– sender of the document

**Receiver **– receiver of the document

**Type** – the document that failed. The documents include orders, acknowledgments, shipments, or invoices.

**Summary** – this will provide the reason why the document failed i.e., validation failed, business rule failed, etc.

**Documents **– this reflects the number of documents that were unsuccessful and share the same failure reason 

**Last Failure** – reflects the date and time stamp of the most recent failure for that document and failure reason 

**View Documents (Button) **– this button is shown on each line of the summary, by clicking the button the user will be shown more detailed information on the failures (defined below)

**ID **– the unique identifier used by Logicbroker. This value is only used in our portal and not sent out to external systems. 

**Reference Number** – typically the PO or PartnerPO. This value is used in both our portal and external systems.

**View (Button)** – use this button to view the document and review or edit information i.e., ship from address, invoice items, billing address, etc. 

**Details (Button)** – use this button to review event details that will help understand why the document failed and what should be changed to ensure success

**Retry** – users have the ability to retry documents directly from the failed document summary. To retry the document, find the line(s) you would like to retry and select the box(es) on the left side of the screen. Once selected you will see the retry button appear on the top right corner of the screen. Click the retry button and select yes on the confirmation screen. 

**Common Failures**

**Business Rule Failed **– 

When the failure reason “Business Rule Failed” is received, users should click on the text and will be redirected to the event details.

The event details will indicate why the document failed, an example of these details are shown in the image below.

The most popular reason for a business rule failure is due to an invalid reason code. To fix this issue, users should select a valid reason code, usually predetermined by your partner, and retry the document. To retry the document navigate to More Actions in the top right corner and selecting Retry from the dropdown.

**Error Transmitting EDI** – 

If you receive the failure reason “Error Transmitting EDI” it could have occurred because an issue has been encountered when sending your document via EDI. This could be due to the maximum number of retry attempts has been exceeded, the action is impossible while not connected, etc.

The most common reasons for receiving this failure are due to internal server errors and MDN errors.

A 500 Internal Server Error indicates that there has been a time out. To fix this failure is to retry the document. To retry the document, navigate to the top right corner of the page and click More Actions, and select Retry from the dropdown.

A MDN error indicates that the document hit your partner's system, but was not fully transmitted. If a MDN error is received then it usually is related to an AS2 certificate issue and the document should be retried. To retry the document, navigate to the top right corner of the page and click More Actions and select Retry from the dropdown.

If you continue to receive a failure for MDN and 500 errors after retrying the documents, you can submit a ticket to [support](/kb/logicbroker/kb-tickets/new?hsLang=en). Please be sure to include your **company name** , **contact information** , **partner** , and the **document number** in question.

**Validation Failed **–   
A validation failure can be related to orders, acknowledgments, shipments, invoices, or inventory. Click the document type below to learn how to fix the failure. _**What document type failed?**_

Order

Acknowledgment

Shipment

Invoice

Inventory

### Order Validation Failed

If you have received an order validation failure, click on the text to review the event details. This will indicate what needs to be fixed. Next, make the appropriate edits and retry the document. To retry the document, navigate to More Actions in the top right corner and select Retry from the dropdown. The images below show the 3 sections that users are able to edit.

### Acknowledgement Validation Failed

If you have received an acknowledgment validation failure, click on the text to review the event details. This will indicate what needs to be fixed. Next, change the status to Ignored and Retry the document with the corrected changes.

### Shipment Validation Failed

If you have received a shipment validation failure, click on the text to review the event details. This will indicate what needs to be fixed. Next, change the status to Ignored and retry the document. To retry the document, navigate to More Actions in the top right corner and select Retry from the dropdown. 

The images below show the 4 sections that users are able to edit.

### Invoice Validation Failed

If you have received an invoice validation failure, click on the text to review the event details. This will indicate what needs to be fixed. Next, change the status to Ignored and **R****etry** the document with the corrected changes.

### Inventory Validation Failure 

If you have received an inventory validation failure, click on the text to review the event details. This will indicate what needs to be fixed. Next, change the status to Ignored and **R****etry** the document with the corrected changes.

**Cannot Over-Ship Lines** – 

If an order has already shipped in Logicbroker, any other shipment that tries to over ship the order will fail and a message similar to the one above will be received. This error may also occur when there is a mistake made with printing shipping labels and a new one needs to be generated. Printing a label triggers shipment creation, causing instances with duplicate shipments.

To fix the failure, select the **“Noncompliant Documents”** from the toolbar at the top of the Dashboard. From here, select the document you would like to view on the page displaying all failures. The most recent event message will read **“Cannot Over-Ship Lines”** and the event details will be similar to the message shown in the image below.

Scroll down to the **“Related Documents”** and see if there is a shipment in a complete status. If so, you will need to compare the failed order with the completed shipment to see if the SKUs and quantity shipped match.

If the SKUs and quantity shipped on the completed shipment match with what is on the order then go to **“Related Documents”** and pull up the failed shipment. From there, navigate to **“More Actions”** and select **“Change Status”** from the dropdown. Set the status of the Failed shipment to **"Ignored"**.

**Invalid Ship Method** – 

When the failure reason is "Invalid Ship Method" this means that there was an issue with the ship method. There are a variety of reasons for this including a custom code was not set up, shipping information was not included, or the method being used is not supported by the trading partner. To resolve this issue, first look at the **Events** under the Message Center. You will see the failure along with detailed information about why it failed. Next, utilize the **ship method mappings** function found under Shipping Options in the Settings area of the Portal. This will showcase the mappings supported by your trading partners as well as the custom code. 

**Failed to Source Items** – 

If the failure reason is indicated as “Failed to Source Items” this means the SKU was not available or was unable to match the SKU to inventory. To resolve this issue, retailers should utilize the **inventory search** function within the Portal to review the quantity available in the feed, shown in the image below.

After reviewing the available inventory, the user should adjust the order to fulfill the amount available and retry the document by navigating to More Actions and select Retry from the dropdown.

Extracting Data from Logicbroker

We understand that this report is used by your organization in many different ways, many times outside of Logicbroker. The Failed Document Summary can easily be exported from the portal by clicking on the **Export Failed Documents** button on the top left-hand side of the screen (shown below).

This will generate a .xlsx file that users can massage and import into their internal reporting systems. The file will contain document identifiers (LogicbrokerKey, Reference Number, LinkKey), sender and receiver information, the document type that failed, the failure reason, details on the failure, and the date.