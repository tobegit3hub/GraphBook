FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Install dependencies
RUN apt-get -y update
RUN apt-get install -y  vim git python3 python3-pip npm

# Install python packages
ADD ./python/requirements.txt /work/python/requirements.txt
RUN pip install -r /work/python/requirements.txt

# Install npm packages
ADD ./frontend/package.json /work/frontend/package.json
RUN cd ./frontend/ && npm install && cd -

# Add source code
ADD . /work/
WORKDIR /work/

# Build front-end
RUN cd ./frontend/ && npm run build && cd -

# Import official topics
RUN cd ./python/server/ && ./import_official_topics.py ./topicland.ini && cd -

# Expose port
EXPOSE 7788

# Run server
CMD ["./python/server/server.py", "./python/server/topicland.ini"]
