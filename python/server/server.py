#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin

import db_service


logger = logging.getLogger("graph_book")

app = Flask(__name__,
            template_folder="./dist/",
            static_folder="./dist",
            static_url_path="")
cors = CORS(app, resources=r'/*')

app.config['CORS_HEADERS'] = 'Content-Type'

# Define parameters
parser = argparse.ArgumentParser()
parser.add_argument(
    "--host",
    default=os.environ.get("HOST", "0.0.0.0"),
    help="The host of the server(eg. 0.0.0.0)")
parser.add_argument(
    "--port",
    default=int(os.environ.get("PORT", "7788")),
    help="The port of the server(eg. 7788)",
    type=int)
parser.add_argument(
    "--debug",
    default=bool(os.environ.get("DEBUG", "false")),
    help="Enable debug for flask or not(eg. true)",
    type=bool)

# Print used arguments
args = parser.parse_args(sys.argv[1:])
for arg in vars(args):
    logger.info("{}: {}".format(arg, getattr(args, arg)))

db_service = db_service.DbService()

"""
# TODO: Integrated with vue single page app
@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")
"""

@app.route('/api/topics', methods=['GET', 'POST'])
@cross_origin()
def handle_topics():
    if request.method == "GET":
        result = {"topics": db_service.get_topics()}
        return jsonify(result)
    elif request.method == "POST":
        name = request.json["name"]
        db_service.create_topic(name)
        return jsonify({"code": 0})

@app.route('/api/topics/<topic>/characters', methods=['GET', 'POST'])
@cross_origin()
def handle_characters(topic):
    if request.method == "GET":
        chosen_characters_names = request.args.getlist('chosen_characters_names[]')
        result = {"characters": db_service.get_characters(topic, chosen_characters_names)}
        return jsonify(result)
    elif request.method == "POST":
        
        if "name" in request.json and "note" in request.json and "image_path" in request.json:
            name = request.json["name"]
            note = request.json["note"]
            image_path = request.json["image_path"]
            db_service.create_character(topic, name, note, image_path)
        elif "insert_characters" in request.json and "update_characters" in request.json and "delete_characters" in request.json:
            insert_characters = request.json["insert_characters"]
            update_characters = request.json["update_characters"]
            delete_characters = request.json["delete_characters"]
            db_service.update_characters(topic, insert_characters, update_characters, delete_characters)
        return jsonify({"code": 0})

@app.route('/api/topics/<topic>/characters/<character>', methods=['GET'])
@cross_origin()
def get_character(topic, character):
    if request.method == "GET":
        result = {
            "character": db_service.get_character(topic, character),
            "upstream_characters": db_service.get_upstream_characters(topic, character),
            "downstream_characters": db_service.get_downstream_characters(topic, character)
        }
        return jsonify(result)

@app.route('/api/topics/<topic>/characters_names', methods=['GET'])
@cross_origin()
def get_characters_names(topic):
    if request.method == "GET":
        chosen_groups = request.args.getlist('chosen_groups[]')
        result = {"characters_names": db_service.get_characters_names_in_groups(topic, chosen_groups)}
        return jsonify(result)

@app.route('/api/topics/<topic>/relations', methods=['GET', 'POST'])
@cross_origin()
def handle_relations(topic):
    if request.method == "GET":
        result = {"relations": db_service.get_relations(topic)}
        return jsonify(result)

    elif request.method == "POST":
        if "source" in request.json and "target" in request.json and "relation" in request.json:
            source = request.json["source"]
            target = request.json["target"]
            relation = request.json["relation"]
            note = request.json["note"]
            db_service.create_relation(topic, source, target, relation, note)

        elif "insert_relations" in request.json and "update_relations" in request.json and "delete_relations" in request.json:
            insert_relations = request.json["insert_relations"]
            update_relations = request.json["update_relations"]
            delete_relations = request.json["delete_relations"]
            db_service.update_relations(topic, insert_relations, update_relations, delete_relations)
        return jsonify({"code": 0})

@app.route('/api/topics/<topic>/groups', methods=['GET', 'POST'])
@cross_origin()
def handle_groups(topic):
    if request.method == "GET":
        result = {"groups": db_service.get_groups(topic)}
        return jsonify(result)
    elif request.method == "POST":
        if "group_name" in request.json and "character_name" in request.json:
            group_name = request.json["group_name"]
            character_name = request.json["character_name"]
            db_service.create_group(topic, group_name, character_name)

        elif "insert_groups" in request.json and "update_groups" in request.json and "delete_groups" in request.json:
            insert_groups = request.json["insert_groups"]
            update_groups = request.json["update_groups"]
            delete_groups = request.json["delete_groups"]
            db_service.update_groups(topic, insert_groups, update_groups, delete_groups)

        return jsonify({"code": 0})

@app.route('/api/topics/<topic>/groups_names', methods=['GET'])
@cross_origin()
def get_groups_names(topic):
    if request.method == "GET":
        result = {"groups": db_service.get_groups_names(topic)}
        return jsonify(result)

@app.route('/api/topics/<topic>/paths', methods=['GET'])
@cross_origin()
def get_node_node_paths(topic):
    if request.method == "GET":
        source = request.args.get('source', type = str)
        target = request.args.get('target', type = str)
        cutoff = request.args.get('cutoff', default = -1, type = int)
        only_directed = request.args.get('only_directed', default = False, type=lambda v: v.lower() == 'true')

        if source and target:
            paths = db_service.compute_paths(topic, source, target, cutoff, only_directed)
            result = {"paths": paths}
        else:
            # TODO: Throw error if failed
            result = {"code": -1}
        return jsonify(result)

@app.route('/api/topics/<topic>/weights', methods=['PUT'])
@cross_origin()
def update_characters_weights(topic):
    if request.method == "PUT":
        db_service.update_characters_weights(topic)
        result = {"code": 0}
        return jsonify(result)


def main():
  # Start web browser if possible
  # webbrowser.open("http://{}:{}".format(args.host, args.port))

  # TODO: debug config does not work
  app.run(host=args.host,
          port=args.port,
          threaded=True,
          debug=args.debug)

if __name__ == "__main__":
  main()
