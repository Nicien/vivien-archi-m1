FROM python:3.13-slim

# Je sais pas 
ENV PIP_DISABLE_PIP_VERSION_CHECK=on 

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /app

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "22222"]