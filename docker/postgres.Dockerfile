FROM postgres:15-alpine

# Install health check dependencies
RUN apk add --no-cache bash

# Copy init scripts
COPY ./database/*.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

