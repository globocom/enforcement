FROM mc706/pipenv-3.8 AS builder
LABEL maintainer="globo.com"

COPY . /build
WORKDIR /build

RUN pipenv lock --requirements > requirements.txt

FROM python:3.8

WORKDIR /src
COPY --from=builder /build .
RUN pip install -r requirements.txt

CMD kopf run main.py --quiet