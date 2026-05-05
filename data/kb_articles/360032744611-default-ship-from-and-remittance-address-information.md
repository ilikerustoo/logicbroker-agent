---
title: "Default Ship From and Remittance Address Information"
url: "https://support.logicbroker.com/kb/logicbroker/360032744611-default-ship-from-and-remittance-address-information"
category: "Platform"
---

March 3, 2026

# Default Ship From and Remittance Address Information

## 

**Setting Default Ship-From and Remit-To Address Information**

Logicbroker has the ability to populate ship-from and remit-to address information based on a one-time setup in your Logicbroker account. The ship-from address is typically used for the creation of shipments and the remit-to (or remittance) address is typically used for the creation of invoices.

**Example of Use**

If you are connected to a retailer that requires a ship-from address and you don't want to have to type in the same ship-from address when you create ever new shipment document, this feature would save time (see the list below on where the information is required in a shipment).

Instead of typing in this information manually or using the address book each time, Logicbroker can pre-populate the fields. This is ideal when you have a primary ship-from address where most of your shipments originate. You can overwrite what is pre-populated as needed as well.

**Setup Process**

  1. Go to Settings -> Account Information: <https://portal.logicbroker.com/profile/account-information>
  2. Scroll down to Document Defaults and select **Ship From Addresses**
     * You can set up a default ship from address for the entire account (regardless of retailer) or you can set up unique default ship-from addresses for each retailer you support.
  3. Enter in the address information. Best practice is to include: 
     * Company Name
     * First Name/Last Name (Contact Name)
     * Address Line 1
     * City/State/Zip
     * Country = US (not USA, not U.S., not U.S.A., not United States)
     * Phone
  4. Click **Save**. 



**IMPORTANT** : This process is the same for setting up a default remit-to address, except that you select **Remittance Address** on the **Account Information** page.