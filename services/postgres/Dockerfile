FROM postgis/postgis

# Install necessary packages for building RUM extension
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-all \
    postgresql-12-rum

# Clone RUM repository from GitHub
RUN git clone https://github.com/postgrespro/rum /tmp/rum

# Change directory to rum
WORKDIR /tmp/rum

# Build and install RUM extension
RUN make USE_PGXS=1
RUN make USE_PGXS=1 install

# Move back to original working directory
WORKDIR /tmp/db

# Ensure correct permissions for the database directory
RUN mkdir /data && chown postgres /data

# Copy over the pagila database;
# we rename the files so that they get executed in the correct order
COPY schema.sql /docker-entrypoint-initdb.d/01.sql
