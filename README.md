# Banking System

## RESTful API Endpoints

### Authentication

- POST /api/login

  - Backend Function: loginUser
  - Request: { "username": "string", "password": "string", "clientId": "string" }
  - Response: { "message": "string", "status": "success"|"error", "accountId": "string", "sessionId": "string", "userType": "customer"|"clerk"|"admin"}

- POST /api/logout
  - Backend Function: logoutUser
  - Request Headers: { "Authorization": "Bearer {sessionId}" }
  - Response: { "message": "string", "status": "success"|"error" }

### Account Management

- POST /api/accounts

  - Backend Function: createAccount
  - Request: { "username": "string", "userType": "customer"|"clerk" }
  - Response: { "message": "string", "status": "success"|"error", "accountId": "string" }

- DELETE /api/accounts/{accountId}

  - Backend Function: deleteAccount
  - Request Headers: { "Authorization": "Bearer {sessionId}" }
  - Response: { "message": "string", "status": "success"|"error" }

- GET /api/accounts/{accountId}/balance

  - Backend Function: getAccountBalance
  - Request Headers: { "Authorization": "Bearer {sessionId}" }
  - Response: { "message": "string", "status": "success"|"error", "balance": "float" }

- POST /api/accounts/transfer
  - Backend Function: transferFunds
  - Request Headers: { "Authorization": "Bearer {sessionId}" }
  - Request: { "sourceAccountId": "string", "destAccountId": "string", "amount": "float" }
  - Response: { "message": "string", "status": "success"|"error" }
