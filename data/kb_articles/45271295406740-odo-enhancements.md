---
title: "ODO Enhancements"
url: "https://support.logicbroker.com/kb/logicbroker/45271295406740-odo-enhancements"
category: "Supplier Onboarding"
---

March 3, 2026

# ODO Enhancements

## 

**Audience****:** Suppliers

Logicbroker is excited to announce new enhancements made to the On-Demand Onboarding process that will improve the overall retailer management and supplier experience. Feedback has been gathered from our users and we have added the following updates to the module:

**Page UI Revamp**

All Onboarding pages have new styling applied to provide a seamless and consistent experience. The main onboarding page features new quick filters and new functionality to use the Saved Search functionality. Now users can set up supplier groups and apply filers on this page to see relevant data. The Supplier Onboarding page now organizes form details in sections to easily navigate. 

**Resending Invitations to New Contacts**

Retailers can now resend invitations to a different contact without needing to restart the process. These are some things to keep in mind when resending an invite to a new contact:

  * the supplier needs to be in an ‘Invite Sent’ status (suppliers that are already onboarding cannot have the primary contact changed)

  * the new email is limited to 1 contact and will replace the existing primary contact




**Show Vendor Number**

Retailers can now easily see and pass over supplier vendor numbers to inventory in stage and production as part of the onboarding process. These are some things to keep in mind:

  * Retailers can optionally add the supplier's vendor number as part of the onboarding invitation on both the individual and bulk invite
  * The vendor number will be displayed from the onboarding list page (can be added as an additional column), the export and the individual supplier page
  * Vendor numbers can be edited from the individual supplier page only when the supplier is in an 'Invite Sent' and 'Form Received' status (once a supplier goes into an 'Onboarding' status, their account is created in stage and this field cannot be edited)
  * Once a supplier is moved to 'Onboarding', the Vendor Number will be added to the Inventory Feed Settings in stage and once moved to 'Live', it will be pushed to production
  * Future updates to vendor number need to be made in the environment the supplier is in as after the initial deploy it will not be pushed into the other environment - those changes will not appear on the individual supplier page



**Connect Supplier to Existing Account**

For suppliers that have been invited but have an active relationship with the retailer, retailers can now connect their existing account instead of having the supplier start over. These are some things to keep in mind:

  * For suppliers in an ‘Invite Sent’ or ‘Form Received’ status, retailers will now see the option to ‘Connect to Existing Account’ from the individual supplier page

  * The retailer can select which existing supplier they want to tie that onboarding to (the list will not show suppliers that are actively onboarding or live)

  * Once connected, the page will update with the existing supplier's data and be pushed into an Onboarding status - all onboarding tasks will also be updated with the supplier's progress so far

  * Email communication will be limited to 'Next Steps' email for stage onboarding and 'Pushed to Prod' email for production onboardings - we will skip the 'Onboarding Invite' and 'User Invite' emails

  * An event will log the connected account from the individual supplier page