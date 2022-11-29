#!/usr/bin/env python3

import fire
from .topicland_client import TopicLandClient

class TopicLandCmd(object):

  def list_topics(self, server):
    client = TopicLandClient(server)
    return client.get_topics()

  def delete_topic(self, server, topic):
    client = TopicLandClient(server)
    return client.delete_topic(topic)

def main():
  fire.Fire(TopicLandCmd)

if __name__ == '__main__':
  main()

