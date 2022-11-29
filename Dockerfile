FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Install dependencies
RUN apt-get -y update
RUN apt-get install -y vim git curl python3 python3-pip npm sqlite3

# Upgrade nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
RUN apt-get install -y nodejs

# Install python packages
ADD ./python/requirements.txt /work/python/requirements.txt
RUN pip install -r /work/python/requirements.txt

# Install npm packages
ADD ./frontend/package.json /work/frontend/package.json
RUN cd /work/frontend/ && npm install

# Add source code
ADD . /work/

# Build front-end
RUN cd /work/frontend/ && npm run build

WORKDIR /work/python/server/

# Import official topics
RUN ./import_official_topics.py ./topicland.ini

# Expose port
EXPOSE 7788

# Run server
CMD ["./server.py", "./topicland.ini"]
