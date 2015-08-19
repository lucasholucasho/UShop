UShop
==============================

Description
-------------

This is a location-based shopping web app that uses the user's location and the Retailigence API to search for nearby products. From the search results page (complete with information about the store and product, along with estimated distance), the user can select a store and request an Uber ride there (thanks Uber API!).

Also, the name that the user sees when they authenticate with their Uber credentials is programmatically retrieved via the User Profile endpoint.


How to run
---------------

1. Download this repository.
2. Go to https://developer.uber.com/ and sign up for an Uber developer account.
3. Register a new Uber application and make your Redirect URL and Privacy Policy URL `http://localhost:7000/submit` - ensure that the `profile`, `history_lite`, and `history` scopes (under "LIST OF UNRESTRICTED SCOPES") are checked off.
4. Make your SURGE CONFIRMATION REDIRECT URI `http://localhost:7000/surge`.
5. In app.json, add your client id and secret (available from the app dashboard) as the environment variables `UBER_CLIENT_ID` and `UBER_CLIENT_SECRET`.
6. In app.json and config.json, change the `name` value to be what you called your application in step 3.
7. Run `export UBER_CLIENT_ID=<UBER_CLIENT_ID in app.json>` and `export UBER_CLIENT_SECRET=<UBER_CLIENT_SECRET in app.json>`
8. Run `pip install -r requirements.txt` to install dependencies
9. Run `python app.py`
10. Navigate to http://localhost:7000 in your browser