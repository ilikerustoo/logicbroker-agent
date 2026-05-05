---
title: "Partner Management Center"
url: "https://support.logicbroker.com/kb/logicbroker/28343921639444-partner-management-center"
category: "Platform"
---

March 3, 2026

# Partner Management Center

## 

**Audience :** Retailers

In this article, you will find information related to the [**Partner Management Center**](https://portal.logicbroker.com/partnermanagementcenter) page. The sections within this article are outlined below:

  * At a Glance
  * Display
  * Settings
  * Actions



### **At a Glance**

The **Partner Management Center** page provides retailers with a place to view and manage their relationships with their suppliers all from a central location. 

### **Display**

**Display**

**Company Name **– supplier account name 

**Score** – Scorecard letter grade based on the date range specified 

**Order Count** – number of orders based on the date range specified 

**Status** – partnership status ('Live' or 'Paused') 

**Type** – supplier's connection to Logicbroker - this is determined by:   
  


  * **Portal** : default 
  * **EDI** : workflow configuration
  * **API** : supplier has a primary key generated (environment specific)
  * **Shopify** : workflow configuration contains 'Shopify'
  * **ShipStation** : workflow configuration contains 'ShipStation'



### **Settings**

****

**Scorecards**

**Shipment Interval (hours) – allowed time to ship in hours**

**Cancellation Percentage – allowed cancellation percentage**

**Exclude Weekends – excludes weekends when calculating the scorecard grade**

**Sourcing Priority**

Retailers can set the sourcing priority for suppliers in the case where there are preferred partners or 1P vs. 3P partners and there's a preference to have orders sourced to some companies over others.   
**  
**

**Requirements :** Your account must be using cost-based sourcing for this functionality to work. It will not work with  SKU-based sourcing since SKU-based sourcing will automatically assign orders to the supplier holding the SKU in their inventory feed.

**Update from scorecards:** Instead of manually setting priority, retailers can choose to automatically set priority sourcing based off scorecard data using a date range. 

### 

### **Actions**

**Generate Report**

This will generate a report for all suppliers using the date range specified on the page and will include all the metrics used to calculate the scorecard grade. 

**Pause Supplier(s)**

Retailers can pause suppliers which will   
  


  * Set inventory to '0' (unless the suspension reason is 'Stale Inventory'
  * Block new orders from being sourced to the supplier
  * Allow suppliers to fulfill existing open orders



**1\. Select Supplier(s):** select an individual supplier to block or select multiple to pause in bulk   


**2\. Select the reason for pausing:** choose one of the following reasons  
  


  * Business closure
  * Holiday/Seasonal
  * SLA Compliance
  * Stale Inventory

**3\. Select suspension dates and times:** Add a start and end date for the suspension (date will be in your time zone) 

**4\. Add a message:** Provide any additional context for the supplier on their suspension 

**5\. Account unpaused:** The supplier will automatically be unpaused on the end date. If the reason for suspension is 'Stale Inventory', their account will automatically be unpaused once they upload/send inventory into Logicbroker. Manually updating SKUs in the portal will not unpause the account. 

**Notifications:**   


  * **Suppliers****– will be notified through email with the Trading Partner Notification and an Event will be created in the portal​**
  * **Retailers** **–** will have suspension 'Events' available from the page as well as through the [Events](https://portal.logicbroker.com/event-management) page​




**Schedules:**   
  


  * **Through the API** – pausing suppliers through the API allows for configuring specific times 
  * **Through the Portal** **– pausing or unpausing suppliers runs every 5 minutes based on the schedule the suspension is set for**