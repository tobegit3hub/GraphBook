#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import pymysql.cursors

import db_service
import model

logger = logging.getLogger("openmldb_server")

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

args = parser.parse_args(sys.argv[1:])
for arg in vars(args):
    logger.info("{}: {}".format(arg, getattr(args, arg)))

db_config = model.DbConfig("localhost", "root", "wawa316", "cyberpunk_edgerunner")
#graph = model.Graph()
#graph.load_from_db(db_config)
db_service = db_service.DbService()

"""
@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")
"""

@app.route('/api/dbs', methods=['GET', 'POST'])
@cross_origin()
def get_dbs():
    if request.method == "GET":
        result = {"dbs": db_service.get_databases(db_config)}
        return jsonify(result)
    elif request.method == "POST":
        db_name = request.json["name"]
        db_service.create_database(db_config, db_name)
        return jsonify({"code": 0})

@app.route('/api/<db>/nodes', methods=['GET', 'POST'])
@cross_origin()
def get_nodes(db):
    if request.method == "GET":
        num = request.args.get('num', default = -1, type = int)
        group_name = request.args.get('group', default = "", type = str)
        chosen_nodes = request.args.getlist('chosen_nodes[]')
        result = {"nodes": db_service.get_nodes_for_frontend(db_config, db, num, group_name, chosen_nodes)}
        return jsonify(result)
    elif request.method == "POST":
        insert_nodes = request.json["insert_nodes"]
        update_nodes = request.json["update_nodes"]
        delete_nodes = request.json["delete_nodes"]
        db_service.update_nodes(db_config, db, insert_nodes, update_nodes, delete_nodes)
        return jsonify({"code": 0})

@app.route('/api/<db>/node_names', methods=['GET'])
@cross_origin()
def get_node_names(db):
    if request.method == "GET":
        chosen_groups = request.args.getlist('chosen_groups[]')
        result = {"nodes": db_service.get_nodes_in_groups(db_config, db, chosen_groups)}
        return jsonify(result)

@app.route('/api/<db>/nodes/<name>/downstream', methods=['GET'])
@cross_origin()
def get_node_downstream(db, name):
    if request.method == "GET":
        result = {"nodes": db_service.get_node_downstream(db_config, db, name)}
        return jsonify(result)

@app.route('/api/<db>/nodes/<name>/upstream', methods=['GET'])
@cross_origin()
def get_node_upstream(db, name):
    if request.method == "GET":
        result = {"nodes": db_service.get_node_upstream(db_config, db, name)}
        return jsonify(result)

@app.route('/api/<db>/nodes/weight', methods=['PUT'])
@cross_origin()
def update_nodes_weight(db):
    if request.method == "PUT":
        db_service.update_nodes_weight(db_config, db)
        result = {"code": 0}
        return jsonify(result)

@app.route('/api/<db>/edges', methods=['GET', 'POST'])
@cross_origin()
def get_edges(db):
    if request.method == "GET":
        result = {"edges": db_service.get_edges_for_frontend(db_config, db)}
        return jsonify(result)
    elif request.method == "POST":
        insert_edges = request.json["insert_edges"]
        update_edges = request.json["update_edges"]
        delete_edges = request.json["delete_edges"]
        db_service.update_edges(db_config, db, insert_edges, update_edges, delete_edges)
        return jsonify({"code": 0})

@app.route('/api/<db>/groups', methods=['GET', 'POST'])
@cross_origin()
def get_groups(db):
    if request.method == "GET":
        result = {"groups": db_service.get_groups_for_frontend(db_config, db)}
        return jsonify(result)
    elif request.method == "POST":
        insert_groups = request.json["insert_groups"]
        update_groups = request.json["update_groups"]
        delete_groups = request.json["delete_groups"]
        db_service.update_groups(db_config, db, insert_groups, update_groups, delete_groups)
        return jsonify({"code": 0})

@app.route('/api/<db>/group_names', methods=['GET'])
@cross_origin()
def get_group_names(db):
    if request.method == "GET":
        result = {"group_names": db_service.get_group_names(db_config, db)}
        return jsonify(result)

@app.route('/api/<db>/paths', methods=['GET'])
@cross_origin()
def get_node_node_paths(db):
    if request.method == "GET":
        source = request.args.get('source', type = str)
        target = request.args.get('target', type = str)
        cutoff = request.args.get('cutoff', default = -1, type = int)
        only_directed = request.args.get('only_directed', default = False, type=lambda v: v.lower() == 'true')

        if source and target:
            paths = db_service.get_node_node_paths(db_config, db, source, target, cutoff, only_directed)
            result = {"paths": paths}
        else:
            # TODO: Throw errors
            result = {"code": -1}
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
