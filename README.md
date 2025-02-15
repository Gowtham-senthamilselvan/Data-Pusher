# Data Pusher - Django Web Application

## Overview
This is a Django web application designed to receive data into the app server for an account and send it across different platforms (destinations) using webhook URLs. The application supports the following features:
- **Account Management**: Create, read, update, and delete accounts.
- **Destination Management**: Add, update, and delete destinations for an account.
- **Data Handling**: Receive JSON data via a POST request and forward it to the configured destinations.

---

## Features

### 1. Account Module
Each account has:
- **Email** (mandatory and unique)
- **Account ID** (automatically generated and unique)
- **Account Name** (mandatory)
- **App Secret Token** (automatically generated)
- **Website** (optional)

### 2. Destination Module
- Each destination belongs to an account.
- An account can have multiple destinations.
- Each destination has:
  - **URL** (mandatory)
  - **HTTP Method** (mandatory: GET, POST, PUT)
  - **Headers** (mandatory, JSON format)

### 3. Data Handler
- Receives JSON data via a POST request.
- Validates the `CL-X-TOKEN` header to authenticate the account.
- Forwards the data to all destinations associated with the account.

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Django 4.0 or higher
- Django REST Framework

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Gowtham-senthamilselvan/Data-Pusher.git
   cd data-pusher
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
5. Start the development server:
    ```bash
    python manage.py runserver
6. Access the application at:
    ```bash
    http://127.0.0.1:8000/

---

## API Endpoints
### 1. Account Management
- Create Account: POST /accounts/

- Request Body:
    ```bash
    {
      "email": "test@example.com",
      "account_name": "Test Account",
      "website": "https://example.com"
    }
- List Accounts: GET /accounts/

- Retrieve Account: GET /accounts/<account_id>/

- Update Account: PUT /accounts/<account_id>/

- Delete Account: DELETE /accounts/<account_id>/
---
### 2. Destination Management
- Create Destination: POST /destinations/

- Request Body:
    ```bash
    {
      "account": "<account_id>",
      "url": "https://webhook.site/your-unique-url",
      "http_method": "POST",
      "headers": {
        "APP_ID": "1234APPID1234",
        "APP_SECRET": "enwdj3bshwer43bjhjs9ereuinkjcnsiurew8s",
        "ACTION": "user.update",
        "Content-Type": "application/json",
        "Accept": "*"
      }
    }
- List Destinations: GET /destinations/

- Retrieve Destinations for an Account: GET /destinations/?account_id=<account_id>

- Update Destination: PUT /destinations/<destination_id>/

- Delete Destination: DELETE /destinations/<destination_id>/
---
### 3. Data Handler
- Receive Data: POST /server/incoming_data/

- Headers:

    - CL-X-TOKEN: <app_secret_token>

- Request Body (JSON):
    ```bash
        {
          "name": "John Doe",
          "email": "john.doe@example.com",
          "action": "user.signup"
        }
---    
## Testing
1. Use tools like Postman or curl to test the API endpoints.

2. For testing webhooks, use Webhook.site to generate a unique URL and inspect incoming requests.
---
## Example Workflow
1. Create an account:
    ```bash
        curl -X POST http://127.0.0.1:8000/accounts/ \
        -H "Content-Type: application/json" \
        -d '{
          "email": "test@example.com",
          "account_name": "Test Account",
          "website": "https://example.com"
        }'

2. Create a destination for the account:
    ```bash
    curl -X POST http://127.0.0.1:8000/destinations/ \
    -H "Content-Type: application/json" \
    -d '{
      "account": "<account_id>",
      "url": "https://webhook.site/your-unique-url",
      "http_method": "POST",
      "headers": {
        "APP_ID": "1234APPID1234",
        "APP_SECRET": "enwdj3bshwer43bjhjs9ereuinkjcnsiurew8s",
        "ACTION": "user.update",
        "Content-Type": "application/json",
        "Accept": "*"
      }
    }'
3. Send data to the /server/incoming_data/ endpoint:

    ```bash
    curl -X POST http://127.0.0.1:8000/server/incoming_data/ \
    -H "Content-Type: application/json" \
    -H "CL-X-TOKEN: <app_secret_token>" \
    -d '{
      "name": "John Doe",
      "email": "john.doe@example.com",
      "action": "user.signup"
    }'
   