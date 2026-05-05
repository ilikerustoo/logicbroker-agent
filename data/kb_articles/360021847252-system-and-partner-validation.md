---
title: "System and Partner Validation"
url: "https://support.logicbroker.com/kb/logicbroker/360021847252-system-and-partner-validation"
category: "Supplier Onboarding"
---

March 3, 2026

# System and Partner Validation

## 

The Logicbroker validation engine allows any data field passing through the system to be checked for compliance. This feature is primarily used to make sure that a supplier network sends data that conforms to a retailer’s data specification. It can also be used to make sure that suppliers receive fields required for their data system. Validation is granular, allowing any company to ensure data received is exactly as specified. Whether it is a range of possible values, a specific length for a data field, or ensuring a value is included, the validation engine allows Logicbroker to validate all data flowing in and out of the system.

**Examples of Use:**

  * Example of Use 1: Expected Ship Date value



You are a retailer and want to make sure all of your suppliers send a value for “Expected Ship Date”. Logicbroker can setup validation ensuring that ExpectedShipDate is always populated on documents received from suppliers. Any suppliers neglecting to send a value for ExpectedShipDate will generate a compliance error.

  * Example of Use 2: Supplier requires specific data



You are a supplier receiving orders from a retailer. Your system requires a specific set of Shipping Codes, otherwise your system may crash. To mitigate potential risk, Logicbroker sets up validation to ensure that all ship codes received on orders are among the specified acceptable codes.

**Setup Process:**

1) Specify which fields on a given document are required

2) Logicbroker will setup validation to ensure these fields are being sent

3) Logicbroker tests the validation against data currently being sent

4) Logicbroker will deploy all validation needed to appropriate environments