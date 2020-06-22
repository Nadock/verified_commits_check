FROM python:3.8-alpine

WORKDIR /opt/app

RUN pip3 install pipenv

COPY Pipfile .
COPY Pipfile.lock .

ARG PIPENV_FLAGS
RUN pipenv install --deploy --system ${PIPENV_FLAGS}

COPY ./src ./src

ENV PYTHON_PATH=/opt/app

ENTRYPOINT [ "python3", "-m", "src.action" ]
