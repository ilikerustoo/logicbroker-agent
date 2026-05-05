---
title: "Partner API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 18
---

# Partner API

Base URL: `https://commerceapi.io`

Endpoints: 18

---

### `GET /api/v3/Partners`

List trading partners

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Partners/CompanyProfile`

Get company profile.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Partners/CompanyProfile`

Update company profile.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `profile` (body, string, required): 

**Request Body:**

```
- **Id**: integer
  Account number.
- **CompanyName**: string
  Company name.
- **Address1**: string
  Address line 1.
- **Address2**: string
  Address line 2.
- **City**: string
  City.
- **State**: string
  State.
- **Zip**: string
  ZIP code.
- **Country**: string
  Country.
- **Phone**: string
  Phone number.
- **Email**: string
  Email address.
- **Description**: string
  Company description.
- **Categories**: array
  List of company categories.
- **Subcategory**: string
  Subcategory.
- **ShareProfile**: boolean
  Set to true to share profile with other companies.
- **Website**: string
  Company website.
- **CustomerServiceContact**: object
  Partner contact
- **ITContact**: object
  Partner contact
- **MerchandiserContact**: object
  Partner contact
- **OperationsContact**: object
  Partner contact
- **PartnershipContact**: object
  Partner contact
- **Closures**: array
  Closure times.
- **Hours**: array
  Operating hours.
- **Warehouses**: array
  Warehouses.
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Partners/CompanyProfile/{partnerId}`

Get company profile for a given partner.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `partnerId` (path, integer, required): Partner account number.

**Responses:**

- `200`: OK
---

### `GET /api/v3/Partners/Invites`

List onboarding invites

Request rate limited to 1 request per second with bursts up to 5 requests.

**Parameters:**

- `pageSize` (query, integer, optional): Page size
- `page` (query, integer, optional): Page starting at 0

**Responses:**

- `200`: OK
---

### `POST /api/v3/Partners/Invites`

Send onboarding invite

Request rate limited to 1 request every 10 seconds with bursts up to 5 requests.

**Parameters:**

- `invite` (body, string, required): 

**Request Body:**

```
- **CompanyName**: string
  Partner company name
- **Email**: string
  Primary user email address
- **Priority**: string
  Onboarding priority
- **RequestedLiveDate**: string
  Requested go live date
```

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Partners/Invites/{id}/AcceptOrReject`

Accept or reject onboarding form.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (path, string, required): Integration identifier
- `request` (body, string, required): Accepting the invitation, true or false

**Request Body:**

```
- **Accept**: boolean
  True to accept the form.
- **RejectionReason**: string
  Rejection reason if applicable.
```

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Partners/Invites/{id}/GoLive`

Push integration live.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (path, string, required): Integration identifier

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Partners/Invites/{id}/ResendForm`

Resend onboarding form.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (path, string, required): Integration identifier

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Partners/Invites/{id}/ResendUserInvite`

Resend user invite.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `id` (path, string, required): Integration identifier

**Responses:**

- `200`: OK
---

### `GET /api/v3/Partners/Scorecards`

List scorecards for a given date range

Request rate limited to 1 request every 10 seconds with bursts up to 5 requests.

**Parameters:**

- `startDate` (query, string, required): Start date
- `endDate` (query, string, required): End date
- `includeBlank` (query, boolean, optional): Include scorecards with no data

**Responses:**

- `200`: OK
---

### `GET /api/v3/Partners/SupplierGroups`

List all partner groups.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Partners/SupplierGroups`

Create partner group.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `group` (body, string, required): 

**Request Body:**

```
- **Name**: string
  Group name.
- **Partners**: array
  Partners in group. Only the Id field is required when updating the list.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Partners/SupplierGroups/{name}`

Delete partner group.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): 

**Responses:**

- `204`: No Content
---

### `PUT /api/v3/Partners/SupplierGroups/{name}`

Update partner group.

Request rate limited to 10 requests per second with bursts up to 100 requests.

**Parameters:**

- `name` (path, string, required): 
- `group` (body, string, required): 

**Request Body:**

```
- **Name**: string
  Group name.
- **Partners**: array
  Partners in group. Only the Id field is required when updating the list.
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Partners/Suspensions`

Get partner suspensions.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Partners/Suspensions`

Create partner suspension.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `suspension` (body, string, required): Suspension details

**Request Body:**

```
- **PartnerId**: integer
  Partner account number.
- **ReasonCode**: string
  Pause reason code.
- **Message**: string
  Message explaining why this partner is paused.
- **StartDate**: string
  Date to start suspension.
- **EndDate**: string
  Date to end suspension.
```

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Partners/Suspensions/{partnerId}`

Delete partner suspension.

Request rate limited to 1 request per second with bursts up to 10 requests.

**Parameters:**

- `partnerId` (path, integer, required): 

**Responses:**

- `204`: No Content
---

