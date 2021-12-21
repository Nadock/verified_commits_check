FROM python:3.10-alpine

WORKDIR /opt/action

RUN pip3 install pipenv==2021.11.23

COPY Pipfile .
COPY Pipfile.lock .

ARG PIPENV_FLAGS
RUN pipenv install --deploy --system ${PIPENV_FLAGS}

COPY ./src ./src

ENV PYTHON_PATH=/opt/action

CMD [ "python3", "-m", "src.action" ]
