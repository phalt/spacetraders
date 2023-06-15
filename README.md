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
```

Test run the application:

```sh
make test_api
```
