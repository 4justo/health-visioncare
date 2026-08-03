FROM postgres:15-alpine

# Install health check dependencies
RUN apk add --no-cache bash

COPY ./database/init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432