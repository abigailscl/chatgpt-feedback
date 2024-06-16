FROM python:3.12

RUN pip install poetry

ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN touch README.md

ENV VIRTUAL_ENV=/opt/env
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN poetry install --no-root

COPY . .

CMD ["fastapi" ,  "run", "app/infraestructure/api/main.py", "--port", "8000", "--reload"]
