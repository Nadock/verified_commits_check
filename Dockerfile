FROM python:3.8-alpine

RUN mkdir /opt/action && pip3 install pipenv

COPY Pipfile /opt/action
COPY Pipfile.lock /opt/action

ARG PIPENV_FLAGS
RUN cd /opt/action && pipenv install --deploy --system ${PIPENV_FLAGS}

COPY ./src /opt/action/src
COPY entrypoint.sh /opt/action

ENV PYTHON_PATH=/opt/action

ENTRYPOINT [ "/opt/action/entrypoint.sh" ]
