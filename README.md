# Simple Login System

An experiment using [FastAPI](https://fastapi.tiangolo.com) combined with [Auth0](https://auth0.com) to create a simple login/logout system.

## Prerequisites

Install the following if you haven't:
- Postgres 9 or above
- Python 3.6 or above
- [virtualenv](https://virtualenv.pypa.io/en/stable/) (optional)

You also need an account on [auth0](https://auth0.com/)

## Installation

1. Clone the repo and create a virtual environment within the folder.
2. Create new Postgres database and run the script in `sql/auth.sql` to create the tables
3. Install the required modules by entering:
```bash
pip install -r requirements.txt
```
4. Copy file `config.json.template` and rename it to `config.json`, and fill in all the necessary config:
```json
{
    "auth0": {
        "domain": "<YOUR-AUTH0-DOMAIN>",
        "audience": "<YOUR-AUTH0-API-IDENTIFIER>"
    },
    "db": {
        "host": "<YOUR-POSTGRES-DB-HOST>",
        "database": "<YOUR-POSTGRES-DB-NAME>",
        "port": "<YOUR-POSTGRES-DB-PORT>",
        "user": "<YOUR-POSTGRES-DB-USER>",
        "password": "<YOUR-POSTGRES-DB-PASSWORD>"
    },
    "session": {
        "secret": "<YOUR-SESSION-SECRET>"
    }
}
```
5. Test the project is ready by running the command `uvicorn main:app --reload` and going to the web address `localhost:8000` in your browser. If successful you should see a Hello World message.

## Acknowledgements

https://dompatmore.com/blog/authenticate-your-fastapi-app-with-auth0

https://github.com/tiangolo/fastapi/issues/754

https://www.postgresqltutorial.com/postgresql-python/
