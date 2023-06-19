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

## TODO

- Set up database for Surveys
- Get SurveyLoop working
- Make MiningLoop take into account any Surveys in the database that are valid
- Convert all date strings to use the src.support.datetime.DateTime object
- NICE: Display euclidean distance in navigation function when navigating somewhere
- Set up database to track which Ships are IDLE or WORKING
- Simple CLI to put a Ship in IDLE
- Make Async MiningLoop worker that takes an array of ship_symbols and works them all
- Make Async MiningLoop grab available ships from Ship database
- Make buy-ship automatically put ship into idle state
