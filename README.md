# Options Pricing API

This repository contains a Flask application that provides APIs for retrieving options expiry dates, strike prices, and price data from a MySQL database. The APIs support CORS and are intended for use in options trading applications.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
  - [Home Page](#home-page)
  - [Get Expiry Dates](#get-expiry-dates)
  - [Get Strikes List](#get-strikes-list)
  - [Get Price Data](#get-price-data)
- [Database Schema](#database-schema)


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

## Configuration

2. Update the database connection details in the get_db_connection() function in app.py:

   def get_db_connection():
    try:
        db_socket = "/cloudsql"
        instance_connection_name = "your-instance-connection-name"
        unix_socket_path = f"{db_socket}/{instance_connection_name}"

        connection = mysql.connector.connect(
            user='root',
            password='your-password',
            database='stock',
            unix_socket=unix_socket_path
        )
        return connection

    except mysql.connector.Error as e:
        return {"error": e}

## API Endpoints

# Home Page
URL: /
Method: GET
Description: Returns a welcome message.
# Get Expiry Dates
URL: /api/expiries
Method: GET
Description: Retrieves a list of expiry dates from the database.
Response:
json
Copy code
[
  {
    "expiry_dates": "2024-06-30"
  },
  {
    "expiry_dates": "2024-07-31"
  }
]
# Get Strikes List
URL: /api/strikes
Method: GET
Parameters:
expiry (string): The selected expiry date.
right0 (string): The option type (call/put).
Description: Retrieves a list of strike prices for the given expiry date and option type.
Response:
json
Copy code
[
  {
    "strikes": 12000
  },
  {
    "strikes": 12500
  }
]
# Get Price Data
URL: /api/price
Method: GET
Parameters:
expiry (string): The selected expiry date.
right1 (string): The option type (call/put).
strike (int): The selected strike price.
Description: Retrieves price data for the given expiry date, option type, and strike price.
Response:
json
Copy code
{
  "stock_code": "XYZ",
  "exchange_code": "NSE",
  "product_type": "OPTIDX",
  "expiry_date": "30-Jun-24",
  "strike_price": 12000,
  "right": "call",
  "ohlc_data": [
    {
      "datetime": "2024-06-25 09:15:00",
      "open": 100,
      "high": 105,
      "low": 95,
      "close": 102,
      "volume": 10000,
      "open_interest": 5000,
      "count": 10
    },
    {
      "datetime": "2024-06-25 09:30:00",
      "open": 102,
      "high": 106,
      "low": 101,
      "close": 104,
      "volume": 12000,
      "open_interest": 5500,
      "count": 15
    }
  ]
} 

## Database Schema

The application assumes the following database schema:

expiry

eid (int, primary key)
expiry_dates (date)
options_type

oid (int, primary key)
f_eid (int, foreign key to expiry)
strikes_list

sid (int, primary key)
ff_eid (int, foreign key to expiry)
f_oid (int, foreign key to options_type)
strikes (int)
table_unique_fsid

f_sid (int, foreign key to strikes_list)
table_name (varchar)
Price tables

Each price table should have the following columns:
d_stockcode (varchar)
d_exchange (varchar)
d_products (varchar)
d_expirydate (date)
d_strikeprice (int)
d_right (varchar)
d_datetime (datetime)
d_open (float)
d_high (float)
d_low (float)
d_close (float)
d_volume (int)
d_openinterest (int)
d_count (int)



