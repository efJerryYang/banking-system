# Project Documentation

This project utilizes a front-end and back-end separation structure. The front-end uses the Vue framework, the back-end is built with the Django framework, and the database uses a local sqlite3 file for storage.

## Frontend

The frontend is based on the Vue framework and runs on port 21486. To start:

```console
$ npm install
$ npm run dev
```

Frontend main components and their corresponding URLs:

| Feature           | URL                    | Description                                                          |
|-------------------|------------------------|----------------------------------------------------------------------|
| Login             | `/login`               | Login for Clerk-registered accounts using username and password      |
| Logout            | `/logout`              | Route to destroy the Token and log out the signed-in account         |
| Dashboard         | `/dashboard`           | The interface for operations post-login                              |
| Create Account    | `/create-account`      | Interface for Clerk to register an account                           |
| Delete Account    | `/delete-account`      | Interface for Clerk to delete an account using the account ID        |
| Account Balance   | `/account/balance`     | Interface for users to view account balance and transaction history  |
| Transfer Funds    | `/account/transfer`    | Interface for users to transfer funds to other accounts              |
| Transaction Hist. | `/account`             | Parent page for Balance and Transfer, displays account transactions  |

In detail, each page's operations and API requests include:

Detailed API endpoints and operations:

- `LoginPage`: Login interface
  - `POST /api/login`: Login API that requires a username and password.
    - No request header requirements
    - Request body: `{ "username": "string", "password": "string", "clientId": "string" }`
  
- `LogoutHandler`: Logout controller
  - `GET /api/logout`: Interface route controller for logging out. Executes the logout function to exit the logged-in status.
    - Request header: provide authenticated sessionId
    - No request body
  
- `CreateAccount`: Interface used by clerk to create users. Invisible to standard users.
  - `POST /api/accounts`: Create a new user based on username and password. New user ID can be viewed from the backend.
    - Request header: provide authenticated sessionId
    - Request body: `{ "username": "string", "userType": "customer"|"clerk" }`
  
- `DeleteAccount`: Interface used by clerk to delete users. Invisible to standard users.
  - `DELETE /api/accounts/{accountId}`: Delete a user based on accountId by the clerk.
    - Request header: provide authenticated sessionId
    - No request body
  
- `TransferFunds`: Transfer funds between accounts.
  - `POST /api/accounts/transfer`: Execute transfer based on accountId, using sessionId fetched from the backend.
    - Request header: provide authenticated sessionId
    - Request body: `{ "destAccountId": "string", "amount": "float" }`
  
- `AccountBalance`: Check account balance.
  - `GET /api/accounts/balance`: Query the current user's balance.
    - Request header: provide authenticated sessionId
    - No request body
  
- `TransactionsTable`: View transaction history.
  - `GET /api/accounts/transactions`: Fetch transaction records based on accountId, differentiating between customer and clerk.
    - Request header: provide authenticated sessionId
    - No request body

## Backend

The backend is constructed using the Django framework, running on port 21485. To start:

```console
$ pip install -r requirements.txt
$ python3 manage.py runserver 21485
```

The primary backend functionalities are implemented in the [api/views.py](https://github.com/efJerryYang/banking-system/blob/main/banking_system_backend/api/views.py) file, which handles requests from the frontend and returns the corresponding results.

Database operations are primarily achieved using the `django.db` models module. This project comprises three models:

- Users: Records bank system user info
  - Fields: username, password, userType, balance
- Transaction: Logs transfer information
  - Fields: sender, receiver, amount, timestamp
- Token: Logs session information of logged-in users
  - Fields: user, key (sessionId), created, expires

## Authentication

One of the most vital functionalities of this project is to authenticate frontend requests and ascertain the identity of the requester, ensuring standard users cannot access or manipulate other accounts, or pose as a Clerk. Typically, authentication uses either cookies or sessions; this project utilizes sessions:

1. **Token Definition**: The backend defines a Token class to log the sessionId, associated user, and the session's expiration date.
2. **SessionID Mapping**: Through Django's database library, a mapping relationship is established between the sessionId and the Token class.
3. **Login & Token Generation**: Upon a successful login request from the frontend, the backend creates a corresponding Token and returns the sessionId to the frontend.
4. **Storing sessionId Locally**: The frontend saves the sessionId locally using `localStorage` and includes it in the `authorization` field of the HTTP request header for subsequent requests.
5. **Backend Verification**: When receiving a request, the backend fetches the associated Token using the sessionId from the request. It then checks the Token to ascertain whether the request is legitimate or an impersonation attempt.
6. **Automatic Authorization**: If the Token hasn't expired, the frontend's main page accesses do not require re-login. The backend will directly validate the user based on their sessionId.
7. **Logout & Token Expiry**: The frontend can invalidate their own Token immediately by accessing the `/api/logout` endpoint.
8. **Security**: The sessionId returned to the frontend is a randomly generated string of alphanumeric characters. As long as users keep their sessionId confidential, unauthorized users will find it hard to impersonate them and gain elevated privileges.

This ensures security as the sessionIds returned to the frontend are randomly generated strings. As long as users don't expose their sessionIds, it's challenging for attackers to impersonate them.
