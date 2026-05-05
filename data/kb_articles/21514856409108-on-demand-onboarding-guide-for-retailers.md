---
title: "On-Demand Onboarding Guide for Retailers"
url: "https://support.logicbroker.com/kb/logicbroker/21514856409108-on-demand-onboarding-guide-for-retailers"
category: "Retailer Onboarding"
---

March 3, 2026

# On-Demand Onboarding Guide for Retailers

## 

**Audience :** Retailers using On-Demand Onboarding

In this article, you will find a step-by-step guide for retailers to onboarding suppliers using On-Demand Onboarding. The sections within this article are outlined below:

####  __ Note:

On-Demand Onboarding is available in stage for Logicbroker retailer customers. For more information on this process and to see a demo, please reach out to [support@logicbroker.com](mailto:support@logicbroker.com). 

### **Retailer - Add permissions**

To use the [**Onboarding** ](https://stageportal.logicbroker.com/onboarding)page in the stage portal, you will need the **integrations/manage** permission enabled under your account. To see your current permissions, go to the portal > **My Profile** > [**Manage Users**](https://stageportal.logicbroker.com/profile/userlogins). If you are missing the **Integrations** permission, reach out to your account manager to have these enabled. Only users with this permissions can enabled them for others.

### **Retailer - Turn on the Trading Partner notification**

To receive supplier onboarding notifications, turn on the **Trading Partner** notification from the [**Notifications** ](https://stageportal.logicbroker.com/profile/notifications)page in the stage portal. The notifications you will be subscribed to shown below. **Note** : Notifications are sent through email and need to be set up on an individual basis. 

**Supplier has completed their Onboarding form**

This email notifies you when a supplier has completed the Onboarding form so you can review and accept/reject the submission   
  


**Supplier has requested to go live**

This email notifies you when a supplier has completed the Onboarding form so you can review and accept/reject the submission   
  


###  **Retailer -****Configure onboarding settings**

Customize your supplier onboarding experience from the [**Onboarding Settings** ](https://stageportal.logicbroker.com/onboarding/settings)page. 

**Tags**

Add tags to your tag library to manage supplier onboardings based on categories, assignee, supplier type, etc. Add these to individual suppliers from the Supplier Onboarding page and view them on the main Onboarding page.   
  


**Supplier Agreement**

Upload a PDF document you want all suppliers to review and sign as part of the onboarding process. This PDF will appear on the Onboarding form for suppliers to review, download and sign. The signee, date and time will appear under the **Onboarding Form** section of the **Supplier's Onboarding** page.   
  


**Stage Message**

Add custom messaging for all your suppliers to view for special instructions, reminders or any other retailer-specific information. Suppliers will see this communication from the **Onboarding Task Manager** in the **Dashboard** page.   
  


**Production Message**

Add custom messaging for all your suppliers to view for production reminders or any other retailer-specific information. Suppliers will see this communication from the **Production Message** section in the **Dashboard** page.   
  


**Onboarding Form**

**Settings**   
If you do not want to have to review and accept/reject supplier's Onboarding form submissions manually, you can toggle on the **Auto-accept onboarding form** setting. This will automatically accept all supplier's Onboarding form submissions, push their account into stage and send next steps communication to supplier to complete onboarding steps.   
  


**Custom Questions**   
You can collect information from your suppliers from the Onboarding form using up to 5 custom questions.   
  


**Note**   


  * All custom question info is available from the main **[Onboarding](https://stageportal.logicbroker.com/onboarding) **page as a **hidden column** and is available to **export**
  * If a question **name is changed** , all existing supplier responses would show with the new name in the portal and in the export
  * If a question **field is changed** , all existing supplier responses will remain the same and all new responses will be collected using the new field
  * If a question **field is set to 'None / Not used'** , this will delete the question from all new supplier forms and hide the information in the portal and the export - this info will be visible again if the question type is added back



**Supplier Reminders**

**Resend Invitation**   
You can configure automatic reminders to be sent out to your suppliers if they have not made progress in the onboarding process.   
  


  * **Resend Invitation** : If enabled, Logicbroker will automatically resend the initial onboarding invitation to the supplier after they've been in an 'Invite Sent' status for x amount of days. 



  * **Onboarding Reminder** : If enabled, Logicbroker will automatically send an onboarding reminder to the supplier after they've been in an 'Onboarding' status for x amount of days. Email subject: Reminder to complete onboarding steps for [Retailer]



  
  


**Notes**

  * After 4 attempts of communication, Logicbroker will stop sending further communication and you will see an alert on the supplier's page letting you know to reach out to the supplier to discuss the partnership. To remove the error, from the supplier's page, click **Retry** in the top right.
  * You can see the number of attempts made to each supplier from the main **Onboarding** page > **Hide/Show Columns** > show **Communication Attempts**. This data is exportable and will reset once the supplier's status has been updated.
  * To disable automatic reminder messages for a specific supplier, go to the supplier's page > **Onboarding Details** > **General** > **Disable Automated Reminders**
  * If automatic reminder messages are disabled by default and you'd like to send a reminder to a specific supplier, go to the supplier's page > in the top right click on **Resend Onboarding Invite** (if the supplier is in an **Invite Sent** status) or **Send Onbaording Reminder** (if the supplier is in an **Onboarding** status).



**Test Cases**

**Supplier-Specific Test Cases**   
By default, all suppliers will see all test cases - if you want certain test cases to be shown to certain suppliers, you can configure that by first enabling test cases by supplier:   
  
Follow the steps below to configure test cases by supplier:   
  


  * **Toggle on test cases by supplier**



  * **Create Test Groups** : Similar to tags, create groups by deciding a name for each supplier group and clicking 'Add' (ex. EDI Suppliers, Parcel Suppliers, etc.)



  * **Assign Groups toTest Cases** : For each of the supplier groups you created, assign them to the test cases you want them to have access to. _**Please note**_ : All groups must be assigned atleast 1 test case  
  

  * **Add Suppliers to Test Groups** : You can assign a supplier to a test group (which will show/hide test cases according to the test group setup) at various points during the onboarding process: 
    * Single invitation
    * Bulk invitation
    * Supplier onboarding page



**Notes**

  * Test case groups can be assigned to a supplier during any part of the onboarding process
  * This will only show/hide test cases so if a supplier started off with all test cases then was added to a test group, Logicbroker will hide the test cases that do not pertain to them
  * If a supplier was added to a test group accidentally, the group can be removed and all test cases will be shown along with any progress made in the past



### **Retailer - Send new supplier onboarding invitation**

From the [**Onboarding**](https://stageportal.logicbroker.com/onboarding) page, click on**Invite Supplier**(single or bulk) and fill out the invite.

**Note : **Only one email is supported.

**Tip** : Requested live date is recommended to set the expectations with the supplier from the beginning. The Note field can be used to send a custom message to the supplier including your supplier number for them, special instructions, reminders, etc.**  
  
**

### **Supplier - Accept invitation and complete Onboarding form**

The supplier will receive an email an email with the subject line **Supplier has been invited to connect with Retailer**. This email includes a brief introduction to Logicbroker, a link to our [**Onboarding Overview**](/kb/logicbroker/20212966534548-Onboarding-Overview?hsLang=en) article, the expected go-live date, any custom communication you added in the **Note** section of the invitation and an overview of where they are in the onboarding process. The supplier will click on **Accept invitation** to fill out the Onboarding form. 

### **Retailer - Accept or reject the Onboarding form submission**

_*If you have the**Auto-accept onboarding form** setting enabled, you can skip this step _

Once the supplier accepts the invitation and submits the Onboarding form, you will receive an email with the subject line **Supplier has completed their Onboarding form**. Click on **Review submission** or find the supplier’s onboarding task in the portal to **Accept** or **Reject** it. 

**If rejected** : enter in the rejection reason. The supplier will receive an email notification with the opportunity to go back and edit their information. You will be notified when they resubmit the form.

### **Supplier - Create a user account**

Once the supplier's form is accepted, the supplier's company account will be created and pushed to the stage environment. The supplier will receive 2 emails:

  * **Welcome to Logicbroker!** \- this is the user activation email to create their username and password
  * **Connect [Supplier] with [Retailer] – Next steps** \- this provides them with next steps and a link to the stage portal



The **Welcome to Logicbroker!** user activation email expires within 7 days. If the supplier fails to register within 7 days, you can resend the user invitation to the **Primary contact** from the **Supplier's Onboarding** page. Once one person in the supplier company has an account, they can invite team members from their side through the [**Manage Users**](https://stageportal.logicbroker.com/profile/userlogins) page in the portal.

### **Supplier - Complete onboarding steps**

The supplier will complete the onboarding tasks show in the **Onboarding Task Manager** found in the [**Dashboard**](https://stageportal.logicbroker.com/) page. Core onboarding steps vary based on retailer. 

### **Supplier - Request to go live**

Once the supplier has completed onboarding steps available in the portal, they will click on the **Request to go live** button from the **Onboarding Task Manager**.

### **Retailer - Approve or reject the supplier's request to go live**

You will receive an email with the subject line **Supplier has requested to go live**. Click on **Review request** or find the supplier’s onboarding task in the portal to **Push supplier live** or **Reject request to go live**.

**If rejected** : enter in the rejection reason. The supplier will receive an email notification with the opportunity to go back and review onboarding steps. You will be notified when they request to go live again.  


### **Supplier - Go live**

Once you have clicked **Push supplier live** , the supplier will receive the email: **Supplier's connection with Retailer is live!**

### **Supplier - Complete production onboarding steps**

The supplier will complete all post-production onboarding steps mentioned in the **Post Go-Live Tasks** section of the **Dashboard**. These steps can include uploading live inventory, configuring production notifications, etc.