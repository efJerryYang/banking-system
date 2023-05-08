# Banking System

## RESTful API Endpoints

### Authentication

- POST /api/login

  - Backend Function: loginUser
  - Request: { "username": "string", "password": "string", "clientId": "string" }
  - Response: { "message": "string", "status": "success"|"error", "accountId": "string", "sessionId": "string", "userType": "customer"|"clerk"|"admin"}

- POST /api/logout
  - Backend Function: logoutUser
  - Request: { "sessionId": "string" }
  - Response: { "message": "string", "status": "success"|"error" }

### Account Management

- POST /api/accounts

  - Backend Function: createAccount
  - Request: { "username": "string", "userType": "customer"|"clerk" }
  - Response: { "message": "string", "status": "success"|"error", "accountId": "string" }

- POST /api/accounts/{accountId}

  - Backend Function: deleteAccount
  - Request: { "sessionId": "string", "accountId": "string" }
  - Response: { "message": "string", "status": "success"|"error" }

- GET /api/accounts/{accountId}/balance

  - Backend Function: getAccountBalance
  - Request: { "sessionId": "string", "accountId": "string" }
  - Response: { "message": "string", "status": "success"|"error", "balance": "float" }

- POST /api/accounts/{sourceAccountId}/transfer
  - Backend Function: transferFunds
  - Request: { "sessionId": "string", "sourceAccountId": "string", "destAccountId": "string", "amount": "float" }
  - Response: { "message": "string", "status": "success"|"error" }
