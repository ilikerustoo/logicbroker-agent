---
title: "Migrating Your Legacy Solution to Logicbroker"
url: "https://support.logicbroker.com/kb/logicbroker/4524737281172-migrating-your-legacy-solution-to-logicbroker"
category: "Platform"
---

March 5, 2026

# Migrating Your Legacy Solution to Logicbroker

## 

Logicbroker supports a wide range of data formats and communication protocols including a fully formed, well-documented API to allow your organization to migrate from your legacy solution quickly and easily to the Logicbroker platform.

Logicbroker’s ability to support JSON, XML, EDI, CSV, and flat files along with communication protocols like RESTful API, AS2, SFTP, and FTP allows your organization to experience a quicker time to value and a higher velocity onboarding than traditional providers.

While Logicbroker does this every day, many organizations like yourself may be doing this for the first time. The purpose of this article is to help your organization assess the true level of effort needed from your technical team to migrate from your current solution to Logicbroker.

### **Transactional Content**

Regardless of your current solution, the transactional content required to be exchanged with your suppliers, customers, sales channels, and/or 3PL’s generally remains unchanged. While each of these supply chain participants may have unique requirements on the formatting of the data and the protocol through which the data is communicated, your organization does not need to retrieve additional data points or manage additional inbound attributes when switching to Logicbroker unless there is additional content that would improve supply chain and eCommerce visibility.

### **Master Integration Formats**

Logicbroker eliminates the need for your organization to manage point-to-point document mapping and the multitude of connection methods that make up your eCommerce dropship and marketplace ecosystem by providing your organization the ability to integrate with Logicbroker using a single master integration format per business transaction. This allows your organization to connect to Logicbroker once and have us connect to an endless number of suppliers, customers, sales channels, and 3PL’s.

### **Testing**

A [stage environment](/kb/logicbroker/360022058031-Environments-Stage-vs-Production?hsLang=en) is provided by Logicbroker at no cost to your organization and is available to test connectivity, business transactions, and business rules before going live. This is helpful not just in the initial migration, but also as your business evolves there may be a need to test additional business document flows, integration format changes, etc.

### **XML/EDI/CSV/Flat File**

If your organization exchanges XML, EDI, CSV’s or flat files with your current provider, Logicbroker can map to these as a part of our platform.

From a technical perspective, the only work that needs to be completed is switching the communication details whether that is AS2, SFTP, or FTP to the Logicbroker provisioned AS2, SFTP, or FTP connection.

  * **Connectivity Details**
    * [AS2 Connectivity Details and Certificate](/kb/logicbroker/360022067691-AS2-Information-EDI-Only-?hsLang=en)
    * [SFTP/FTP Connectivity Details](/kb/logicbroker/360022067631-SFTP-FTP?hsLang=en)



### **API**

If your organization connects to your current provider via API today, there are a few technical changes that need to take place. As we mentioned earlier in this document, the transactional content generally remains unchanged, so the effort can be broken down into two tasks: field name changes and endpoint connectivity.

  * **Field Name Changes  
  
** There will likely be field name changes that need put in place to accommodate for Logicbroker’s API formats. While the content itself isn’t changing, some of the field names may change. For example, your current provider may be looking for the order number passed in a field named “OrderId” while Logicbroker is looking for that to be communicated in a field named “OrderNumber”.  
  
To lower the level of effort involved in field name changes, Logicbroker has publicly available [Swagger (OpenAPI) documentation](https://stage.commerceapi.io/swagger/ui/index) for each endpoint. This can be imported directly into Visual Studio or other IDE’s so that the API endpoints and field names do not need to be added from scratch.  
  



  * **Request Rate Details  
  
** Details on rate request size and limits can be found in the Swagger documentation in the “Implementation Notes” section.  
  
  
  

  * **Endpoint Connectivity  
  
** Rather than connecting to your legacy provider’s endpoints, your organization will need to connect to Logicbroker’s endpoints. These endpoints along with details on: authentication, responses, and actions can be found in our publicly available [Postman project](https://dev.logicbroker.com/?__hstc=233546881.e1f5f40af0e38d651c4b286ccd3bffb6.1762765967593.1772694410339.1772704584277.86&__hssc=233546881.73.1772704584277&__hsfp=86f5b137dcb7b269b3ed43a0d78f3092).