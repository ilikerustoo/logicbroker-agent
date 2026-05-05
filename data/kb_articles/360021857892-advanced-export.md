---
title: "Advanced Export"
url: "https://support.logicbroker.com/kb/logicbroker/360021857892-advanced-export"
category: "Platform"
---

March 3, 2026

# Advanced Export

## 

The Advanced Export section of the Portal can be used to download system data in a variety of formats, including CSV, XLSX, XML, and JSON. It can also be used to create template profiles that can be used to download specific data for reports, imports, and other activities.

1\. Navigate to **Reporting** > **Advanced Export**

2\. From the main **Advanced Export** screen, there are a variety of sections.

  * **Profile** : There are several templates that are automatically provided. Click on the drop down arrow in the Profile box. 
    * **NOTE** : You can create custom export profiles. See Step 8 below.
  * **Output Format** : You can select the preferred output based on your needs. The average user will prefer the XLSX format. 
  * **Document Filter** : Filters allow you to pull data by date range, only look at certain orders in a certain order status, etc. 
    * **NOTE** : Including a**Start Date** and **End Date** filter is key to a successful export.
  * **Fields to Export** : Almost any piece of data on an order, shipment, acknowledgement, etc. can be a field to export. We provide a standard set in the automatically-provided profiles, but you can create custom profiles. 



3\. From the **Profile** section, choose the profile that you would like to use from the drop down menu. Once selected, you will notice that many of the other sections pre-populate based on the profile you selected.

4\. Select your preferred export format.

5\. Adjust the filters as needed, either by adding, removing, or changing what is there. We recommend adding in a **Start Date** and **End Date**. If you are not sure of the document **Status Code** you want, the primary ones used are:

  * **500** = Ready to Ship
  * **1000** = Complete
  * **1100** = Cancelled
  * **1200** = Failed
  * **1400** = Ignored



NOTE: If the filter for **Status Code** is "is not failed" that would show all documents that are Cancelled, Complete, Ignored, etc. If the filter for **Status Code** is "is failed" that would show only the failed documents.

6\. When one of the automatically-provided profiles is selected (Default FTP Order Export, for example), the listing of all of the fields that are included in the report show up under **Fields to Export**. You can configure the report to meet your needs and you are able to add or delete fields to the report. In order to aid in reporting, the field names (aka headers) can be changed using the Alias field.

7\. Once your report is customized to your needs, click on **Download** in the **Output Format** section.

8\. Before leaving the page, if you want to save the new profile you've created, you may do so. Typically users will make customized changes to their reports and then save them so they can be easily loaded again the next time they are to be used. From the **Profile** section, click on **Save As.**

9\. Name your new profile, which is what will appear in the Profile drop-down going forward. 

10\. Going forward, this new profile will be available for use. You may also share this report with others by clicking on **Save to File** , then sending the file to other users who can **Load From File**. This allows people to share the exports and reports that work best for each person.