# System Design

## Overview

Deadline: May 16, 2023

Components: client, web server, database

Submit:

- design document (2 pages maximum)
  - system structure
  - design
  - implementation
  - names (or student IDs)
  - URL of your system
- full program list (client and server)

## Client

### Operations

Suggested operations:

> - accnt_num = open_account(user_name)
> - delete_account(accnt_num)
> - bal = balance(accnt_num)
> - transfer(source_accnt, dest_accnt, amnt)

Ours:

- `account_id = create_account(user_name)` (clerk)
  - or user can `open_account()`, but need a clerk to finish the procedure using `create_account(user_name)`
- `delete_account(account_id)` (clerk)
  - or user can `close_account()`, but need a clerk to finish the procedure using `delete_account(account_id)`
- `bal = balance(account_id)`
- `transfer(source_account_id, dest_account_id, amount)`

### Users

- customers
- bank-clerks

> Only bank clerks have authority to open or delete accounts (customers can only use “balance” or “transfer” operations).

- authentication and access control

  - ~~JWT(JSON Web Token)~~
  - Session tracking
    - username
    - session id
    - expiration time

- No need to use SSL

## Web Server

- Session management

  - Session tracking
    - username
    - session id
    - expiration time
  - ~~JWT(JSON Web Token)~~

- Receive requests from the client (Spring Boot)

  - login
    - GET - login page
      - Response data:
        - info: ok, error
    - POST - login
      - Data
        - username
        - encrypted_password (?)
        - client_id (a user may have multiple clients)
      - Response data:
        - info: ok, error
  - (duplicate?) authentication
  - logout
    - GET - logout
  - manage_account
    - GET - manage_account page for clerk / customer
    - create_account (clerk)
      - POST - create_account
    - delete_account (clerk)
      - POST - delete_account
    - balance (both clerk and customer)
      - POST - balance
    - transfer (both clerk and customer)
      - POST - transfer

- Access the DBMS system via JDBC (Mybatis and Mybatis-Plus)

## RESTful API Endpoints

### Authentication

- POST /api/login

  - Backend Function: loginUser
  - Request: { "username": "string", "password": "string", "clientId": "string" }
  - Response: { "message": "string", "status": "success"|"error", "sessionId": "string" }

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
