# Spacetraders

## Set up

```sh
python3.11 -m venv .venv
source .venv/bin/activate
make install
```

Set up your environment variables in a file called `env.ini` in the root of this project.

```ini
[api]
key = ASK_PAUL_FOR_KEY

[time]
; Show timestamps in this timezone
zone = "Pacific/Auckland"
```

Test run the application:

```sh
make test_api
```

## Simple mining loop

* Register as a new agent: 

```sh
make query q='register'
```

Copy the results of this into a `env.ini` file in the project directory. This is your API key for your agent.

* View you agent details

```sh
make query q='me'
```

* Purchase a ship

Note: As of 17/06/2023 you start with a probe at a shipyard, usually you need a ship at a shipyard to buy new ships.
You will n
