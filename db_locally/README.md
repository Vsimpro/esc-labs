# Database exists locally

These labs have a local SQLite database that the API fetches from. This results in smaller margins, and reduced variance in request resolving time.


## Documentation:

There are two API endpoints:
- `search?email=`
    - Searches for an email in the database.
- `reset?email=`
    - Searches for an email in the database.
    - "Sends" out an password reset link via "email" (not actually)

Both take in a GET parameter like this `<API>/reset?email=ntwamel@example.com`, and return a string. The string does not change in any way between queries.


## Which emails to test:

There are two wordlists included that are made for specially testing these labs. There is "not_in_database.txt" and "in_database.txt". Former includes emails that are not included in the databsae, and the latter are emails that _for sure_ are inside the database. The database consists of ~1000 randomly generated gibberish emails alongside these provided in the text file.