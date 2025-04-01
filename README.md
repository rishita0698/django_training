# Expense sharing application

## Overview
Expense Splitter is a RESTful API designed to simplify group expense management. Whether it’s a trip, party, or any shared event, this application helps track expenditures, split costs fairly, and settle payments effortlessly.

Users can either distribute expenses equally among participants or customize the split based on individual shares. The system categorizes expenses under Occasions (optional) or direct Events, ensuring flexibility in expense tracking.

## Key Highlights:
1. Seamless Expense Tracking – Log expenditures under shared occasions or standalone events.
2. Flexible Cost Splitting – Divide expenses equally or assign custom amounts per participant.
3. Easy Settlements – Track outstanding balances and process payments seamlessly.
4. Intuitive API Design – A clean and efficient REST API built with Django Rest Framework (DRF).

The system revolves around two user roles:
1. Expender – The person who pays for an expense.
2. Utilizer – The individuals who benefit from the expense and owe a share of it.

With Expense Splitter, managing group finances becomes hassle-free, ensuring fair cost-sharing and transparency.

## Table of Contents
- [Features](#features)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [API Endpoint](#api-endpoint)

## Features
1. User Authentication (JWT-based login and signup using Django Rest Framework)
2. Create Occasions to categorize expenses
3. Add Expenditures under occasions or standalone events
4. Expense Splitting (equally or custom-defined shares)
5. Settle Expenses
6. View Summary of expenses for an occasion or event


## Database Schema
The application follows the given schema:

```
sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE occasions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    created_by UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    occasion_id UUID REFERENCES occasions(id) ON DELETE SET NULL, -- Nullable if no occasion
    expender_id UUID REFERENCES users(id) ON DELETE CASCADE, -- Who paid
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event_utilizers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    utilizer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL -- Custom split amount,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    payee_id UUID REFERENCES users(id) ON DELETE CASCADE,
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Installation
### Prerequisites
- Python 3.13.2
- Django
- Django Rest Framework
- JWT Authentication

### Installation Steps
1. Clone the repository:
   git clone https://github.com/rishita0698/django_training.git

2. choose the development branch 
    git checkout development

3. Create and activate a virtual environment 
   python -m venv venv
   venv\Scripts\activate

4. Install the required dependencies:
    pip install -r requirements.txt

5. Navigate to the project directory:
    cd expenseTracker

6. Apply migrations:
    python manage.py migrate

7. Run the development server
    python manage.py runserver

8. Access the API at
    http://127.0.0.1:8000/


## API Endpoint

### User Management
1. /auth/register/ (POST) -	User registration
2. /auth/login/	(POST) - User login
3. /auth/logout/ (POST) – User logout
4. /users/{id}/ (GET) – Fetch user details
5. /users/ (GET) - List all the users

### Occasions Management
1. /expenses/occasions/	(POST)	Create an occasion
2. /expenses/occasions/{id}/	GET	(Get) occasion details
3. /expenses/occasions/{id}/update/ (PUT/PATCH) – Update occasion details
4. /expenses/occasions/{id}/delete/ (DELETE) – Delete an occasion
5. /expenses/occasions/ (GET) – Get a list of all occasions created by the user

### Event Management 
1. /expenses/events/	(POST)	Create an event with utilizers split
2. /expenses/events/{id}/	(GET)	Get event details with all utilzers
3. /expenses/events/{id}/update/ (PUT/PATCH) – Update event details with utilizers if needed
4. /expenses/events/{id}/delete/ (DELETE) – Delete an event
5. /expenses/events/ (GET) – Get all events

### Summaries 
1. /expenses/occasions/{id}/summary/ (GET) – Expense summary for an occasion


### Payments
1. /expenses/payment/clear_expense (POST) - Clean an expense of payer to payee for an event
2. /expenses/payment/ (GET) - List all the payments for a user (received + sent)

