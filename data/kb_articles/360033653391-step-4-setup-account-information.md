---
title: "Step 4: Setup Account Informaton"
url: "https://support.logicbroker.com/kb/logicbroker/360033653391-step-4-setup-account-information"
category: "Supplier Onboarding"
---

March 10, 2026

# Step 4: Setup Account Informaton

## 

In some cases to make processing shipments and invoices easier; we allow to default payment terms, remit to and ship from addresses across all retail channels. To learn more about each see below.

  * Edit Payment Terms
  * Edit Remit To Addresses
  * Edit Ship From Addresses



##### Edit Payment Terms

Under **Settings** > **Account Information** you can setup default payment terms across all your retail channels. Under **Default Payment Terms** , you can default across all retail channels or enter **Partner Specific Payment Terms**.

Setting default payment terms will be used in 3 different scenarios. 

  1. If you are **creating invoices automatically** off of a shipment or order. Setting your payment terms can be configured per retail channel. This will allow you to send the terms of your invoices without requiring any manual effort.
  2. If you are **creating invoices in the portal**. Being that payment terms per retail channel do not change often, it is best to default these to ensure they are always being sent on your invoices.
  3. If you are **not sending** your payment terms through any of the normal integrated methods (CSV, XML, JSON, API, EDI). The fields that you can default are listed below.



#### 🗒️Note:

If you send an invoice with any of the values below, then none will default. For example, if you send N30 in **PaymentTerm.TermsDescription** and have a value of "30" set for **Net Days Due** , the "30" will not default in **PaymentTerm.PayInNumberOfDays**. You will need to leave all values **blank** to have the fields default.

**Field** |  **API Field** |  **Description**  
---|---|---  
**Terms Description** |  PaymentTerm.TermsDescription |  Description of the payment terms. This will be a free form description.  
**Net Days Due** |  PaymentTerm.PayInNumberOfDays |  Number of days in which the invoice is due, before additional charges are accrued.  
**Net Discount Days Due** |  PaymentTerm.DueDate |  Discount days due when discount will be applied.  
**Discount Percentage** |  Discounts.DiscountPercent |  Discount percent will be used as part of the payment terms. It will be used with the discount due date and discount days due.  
  
##### 

##### Edit Remittance Address

Under **Settings** > **Account Information** you can setup default your remittance across all your retail channels. Under **Default Remit To Address** , you can default across all retail channels or enter **Partner Specific Remit To Addresses**.

Setting default remit to addresses will be used in 3 different scenarios. 

  1. If you are **creating invoices automatically** off of a shipment or order. Setting your remit to address can be configured per retail channel. This will allow you to send the address on your invoices without requiring any manual effort.
  2. If you are **creating invoices in the portal**. If you are creating a lot of invoices in the portal a few additional clicks can make creating invoices more time consuming. If you have a defaulted address, there will be no need to click through the address books.
  3. If you are **not sending** your address through any of the normal integrated methods (CSV, XML, JSON, API, EDI). The fields that you can default are listed below.



#### 🗒️Note:

If you send an invoice with any of the values below, then none will default. For example, if you send "Acme Co" in **RemitToAddress.CompanyName** and have a value of "1 Enterprise Dr." set for **Address Line 1** , the "1 Enterprise Dr." will not default in **RemitToAddress.Address1**. You will need to leave all values **blank** to have the fields default.

**Field** |  **API Field**  
---|---  
**Company Name** |  RemitToAddress.CompanyName  
**First Name** |  RemitToAddress.FirstName  
**Last Name** |  RemitToAddress.LastName  
**Address Line 1** |  RemitToAddress.Address1  
**Address Line 2** |  RemitToAddress.Address2  
**City** |  RemitToAddress.City  
**State** |  RemitToAddress.State  
**Zip Code** |  RemitToAddress.Zip  
**Country** |  RemitToAddress.Country  
**Email** |  RemitToAddress.Email  
**Phone** |  RemitToAddress.Phone  
**Address Code** |  RemitToAddress.AddressCode  
  
##### 

##### Edit Ship From Addresses

Under **Settings** > **Account Information** you can setup default your remittance across all your retail channels. Under **Default Ship From Address** , you can default across all retail channels or enter **Partner Specific Ship From Addresses**.

Setting default ship from addresses will be used in 3 different scenarios:

  1. If you are **creating shipments in the portal**. If you are creating a lot of shipments in the portal a few additional clicks can make creating shipments more time consuming. If you have a defaulted address, there will be no need to click through the address books; it will be auto-loaded once draft is created.
  2. If you are **not sending** your address through any of the normal integrated methods (CSV, XML, JSON, API, EDI, or system). The fields that you can default are listed below.



#### 🗒️Note:

If you send an shipment with any of the values below, then none will default. For example, if you send "Acme Co" in **ShipFromAddress.CompanyName** and have a value of "1 Enterprise Dr." set for **Address Line 1** , the "1 Enterprise Dr." will not default in **ShipFromAddress.Address1**. You will need to leave all values **blank** to have the fields default.

**Field** |  **API Field**  
---|---  
**Company Name** |  ShipFromAddress.CompanyName  
**First Name** |  ShipFromAddress.FirstName  
**Last Name** |  ShipFromAddress.LastName  
**Address Line 1** |  ShipFromAddress.Address1  
**Address Line 2** |  ShipFromAddress.Address2  
**City** |  ShipFromAddress.City  
**State** |  ShipFromAddress.State  
**Zip Code** |  ShipFromAddress.Zip  
**Country** |  ShipFromAddress.Country  
**Email** |  ShipFromAddress.Email  
**Phone** |  ShipFromAddress.Phone  
**Address Code** |  ShipFromAddress.AddressCode