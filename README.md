# spares-ecommerce

## Development setup

This project uses [uv](https://docs.astral.sh/uv/) and Python 3.14.

Install the locked dependencies and create the virtual environment:

```sh
uv sync
```

Before running Django, configure `SECRET_KEY`, `EMAIL_HOST`, `EMAIL_PORT`,
`EMAIL_USE_SSL`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` in a local `.env`
file. Then run migrations and start the development server:

```sh
uv run python manage.py migrate
uv run python manage.py runserver
```