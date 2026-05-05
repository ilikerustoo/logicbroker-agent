---
title: "Business Rule Engine"
url: "https://support.logicbroker.com/kb/logicbroker/360022068871-business-rule-engine"
category: "Platform"
---

March 3, 2026

# Business Rule Engine

## 

**Business Rule Engine**

Business rules are a feature of the Logicbroker platform that allows retailers and suppliers to more easily map to each other’s specifications. There may be times when one trading partner requires a value that is not contained within your schema, if this is the case, you may request that Logicbroker see if Business Rules are able to assist with the mapping.

**Example of Use**

You are a supplier and you send a fulfillment code on each line item. Since you are connected to different retail channels, each retailer requires a different fulfillment code than the standard you send Logicbroker. Logicbroker can then employ a business rule for each of your retail channels that correctly maps to the retailers specification.

_Logicbroker would implement the above to fulfill the requirement for each retailer you are connected with_

**Example 2: Creating Container codes**

Logicbroker will make sure that you’re tracking numbers and container codes meet G1 requirements if you are trading with a Retailer that requires specific container codes per boxes. This is useful when your system is unable to provide detailed container information. Logicbroker can then use business rules to insert this data, where required based on your retailers specifications.

**Setup Process**

  1. Identify Business Rule requirements
  2. Write business rule and test within Business Rule environment
  3. Deploy Rule to stage environment for Stage testing
  4. Validate stage process
  5. Deploy Rule to Production