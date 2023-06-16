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

## Automation

Most of the game loop can be found in the `src/logic/` directory.
I'e tried to standardise "actions" to perform so you can build up a list of actions
and run it.

You can run the automation like this:

```sh
make automate
``

Worth noting that in the automation stack things are async.
