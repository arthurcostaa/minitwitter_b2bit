FROM python:3.13-slim

RUN mkdir /app

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


COPY ./pyproject.toml ./poetry.lock ./

RUN pip install poetry && \
    poetry config installer.max-workers 10 && \
    poetry install --only main --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--reload"]