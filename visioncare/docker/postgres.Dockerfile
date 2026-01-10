FROM postgres:15-alpine

RUN apk add --no-cache bash

COPY ./database/*.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
