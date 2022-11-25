# Topic Land

**TopicLand** is the tool to manage and explore topics with knowledge graphs and so on.

It is recommanded to record and explore complex topics such as *novels*, *movies*, *TV series* and *games*.

* Clarify the relations of characters with [Knowledge Graph](https://en.wikipedia.org/wiki/Knowledge_graph).
* Use [PageRanke](https://en.wikipedia.org/wiki/PageRank) or other algorithms to select out the prominent roles. 
* Find the shortest path or all paths with [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) for any character.
* Persistent your knowledge graphs for custom topics and share with others.

![](./images/play_graph.gif)

## Install

Build from scratch.

```
git clone https://github.com/topicland/TopicLand.git

cd ./TopicLand/frontend/
npm install
npm run build

cd ../python/server/
pip install -r ../requirements.txt
./server.py ./topicland.ini
```

Load official topics.

```
git submodule update --init

cd ./python/server/
./import_official_topics.py ./topicland.ini
```

## Usage

Explore the offical topics.

![](./images/topic_list.jpg)

Create a new topic.

![](./images/create_topic.jpg)

Add some characters and connect with relations.

![](./images/add_character.jpg)

View the knowledge graph and play the animation.

![](./images/view_graph.jpg)

Check out the detail of characters.

![](./images/character_list.jpg)

![](./images/character_detail.jpg)

## Contribution

* Web developers and designers are required to beautify the web pages.
* Content editors are welcome to add more outstanding topics.

Feel free to submit Issues or Pull-requests and any feedback is welcome.

