---
title: "User API"
source_url: "https://commerceapi.io/swagger/docs/v3"
api_version: "v3"
base_url: "https://commerceapi.io"
endpoints_count: 5
---

# User API

Base URL: `https://commerceapi.io`

Endpoints: 5

---

### `GET /api/v3/Users`

Get all users.

Request rate limited to 1 request per second with bursts up to 5 requests.

**Responses:**

- `200`: OK
---

### `POST /api/v3/Users`

Invite a new user.

Request rate limited to 1 request per second with bursts up to 5 requests.

**Parameters:**

- `request` (body, string, required): 

**Request Body:**

```
- **Email**: string
  Email address.
- **Permissions**: array
  User permissions list.
```

**Responses:**

- `200`: OK
---

### `GET /api/v3/Users/Export`

Export all users.

Request rate limited to 1 request per second with bursts up to 5 requests.

**Parameters:**

- `fileType` (query, string, optional): CSV or XLSX.

**Responses:**

- `200`: OK
---

### `DELETE /api/v3/Users/{id}`

Delete a user.

Request rate limited to 1 request per second with bursts up to 5 requests.

**Parameters:**

- `id` (path, string, required): User id

**Responses:**

- `200`: OK
---

### `PUT /api/v3/Users/{id}`

Update profile for a user.

Request rate limited to 1 request per second with bursts up to 5 requests.

**Parameters:**

- `id` (path, string, required): User id
- `request` (body, string, required): 

**Request Body:**

```
- **FirstName**: string
  First name.
- **LastName**: string
  Last name.
- **Permissions**: array
  Permissions list.
- **Groups**: array
  Groups list.
```

**Responses:**

- `200`: OK
---

