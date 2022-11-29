import requests

class TopicLandClient(object):

    def __init__(self, server) -> None:
        self.server = server

    def get_topics(self):
        url = "{}/api/topics".format(self.server)
        response = requests.get(url)
        return response.json()["topics"]

    def delete_topic(self, topic):
        url = "{}/api/topics/{}".format(self.server, topic)
        response = requests.delete(url)
        return response.json()