from array import array
import csv
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy import text
import shutil
import networkx_util
import pandas as pd

logging.basicConfig(level=logging.INFO)

"""
The configuration of database, support SQLite and Mysql.
"""
class DbConfig(object):
    def __init__(self, dbms: str, endpoint: str, username: str = "", password: str = "", db_name: str = "graph_book") -> None:
        self.dbms = dbms.lower()
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.db_name = db_name

        self.check_dbms()

    @staticmethod
    def create_default_config():
        return DbConfig("sqlite", "graph_book.db")

    """
    Check if the DBMS is supported or not.
    """
    def check_dbms(self) -> None:
        SUPPORTED_DBMS_LIST = ["sqlite", "mysql"]
        if self.dbms not in SUPPORTED_DBMS_LIST:
            raise Exception("DBMS {} is not supported, supported list is {}".format(
                self.dbms, SUPPORTED_DBMS_LIST))


"""
The helper class to interative with database.
"""
class DbService(object):
    def __init__(self, db_config: DbConfig) -> None:
        self.db_config = db_config
        self.engine = None
        self.init_engine()
        self.init_database()
        self.init_tables()

    def init_engine(self):
        config = self.db_config
        if config.dbms == "sqlite":
            engine_url = "sqlite+pysqlite:///{}".format(config.endpoint)
            self.engine = create_engine(engine_url, echo=True, future=True)
        elif config.dbms == "mysql":
            engine_url = "mysql+pymysql://{}:{}@{}/{}".format(
                config.username, config.password, config.endpoint, config.db_name)
            self.engine = create_engine(
                engine_url, echo=True, future=True, pool_size=100, max_overflow=0)

    """
    Create the internal database.
    """
    def init_database(self) -> None:
        if self.db_config.dbms == "sqlite":
            # No need to create database for sqlite
            pass

        elif self.db_config.dbms == "mysql":
            # Connect without default database
            engine_url = "mysql+pymysql://{}:{}@{}".format(
                self.db_config.username, self.db_config.password, self.db_config.endpoint)
            engine = create_engine(
                engine_url, echo=True, future=True, pool_size=100, max_overflow=0)
            conn = engine.connect()

            sql = "CREATE DATABASE IF NOT EXISTS `{}`".format(self.db_config.db_name)
            conn.execute(text(sql))
            conn.close()

    """
    Create the internal tables.
    """
    def init_tables(self) -> None:
        conn = self.engine.connect()

        sql = """
        CREATE TABLE IF NOT EXISTS `topics` (
            `name` varchar(64) NOT NULL,
            PRIMARY KEY (`name`)
        );
        """
        conn.execute(text(sql))

        sql = """
        CREATE TABLE IF NOT EXISTS `characters` (
            `topic` varchar(64) NOT NULL,
            `name` varchar(64) NOT NULL,
            `weight` float DEFAULT NULL,
            `note` varchar(4096) DEFAULT NULL,
            `image_name` varchar(4096) DEFAULT NULL,
            PRIMARY KEY (`topic`, `name`),
            CONSTRAINT `fk_characters_topic` FOREIGN KEY (`topic`) REFERENCES `topics`(`name`)
        );
        """
        conn.execute(text(sql))

        sql = """
        CREATE TABLE IF NOT EXISTS `relations` (
            `topic` varchar(64) NOT NULL,
            `source` varchar(64) NOT NULL,
            `target` varchar(64) NOT NULL,
            `relation` varchar(64) NOT NULL,
            `note` varchar(4096) DEFAULT NULL,
            PRIMARY KEY (`topic`, `source`, `target`),
            CONSTRAINT `fk_relations_topic` FOREIGN KEY (`topic`) REFERENCES `topics`(`name`)
        );
        """
        conn.execute(text(sql))

        sql = """
        CREATE TABLE IF NOT EXISTS `groupx` (
            `topic` varchar(64) NOT NULL,
            `group_name` varchar(64) NOT NULL,
            `character_name` varchar(64) NOT NULL,
            PRIMARY KEY (`topic`, `group_name`, `character_name`),
            CONSTRAINT `fk_groupx_topic` FOREIGN KEY (`topic`) REFERENCES `topics`(`name`)
        )
        """
        conn.execute(text(sql))

        conn.commit()
        conn.close()

    """
    Get all topics.
    """
    def get_topics(self) -> list:
        conn = self.engine.connect()
        sql = "SELECT name FROM topics"
        result = conn.execute(text(sql))
        return [t[0] for t in result.all()]

    """
    Get statistics of all topics.

    Return data should be like this:
        {
            count: 2,
            statistic: [
                {
                    "name": "topic_a",
                    "characters": 10,
                    "relations": 20,
                    "groups": 5
                },
                {
                    "name": "topic_b",
                    "characters": 20,
                    "relations": 30,
                    "groups": 0
                }
            ]
        }
    """
    def get_topics_statistics(self) -> map:
        conn = self.engine.connect()
        sql = "SELECT name FROM topics"
        result = conn.execute(text(sql)).all()
        topic_count = len(result)
        statistics = {}
        for item in result:
            topic_name = item[0]
            statistics[topic_name] = {
                "topic": topic_name,
                "characters": 0,
                "relations": 0,
                "groups": 0
            }

        sql = "SELECT topic, count(*) FROM characters GROUP BY topic"
        result = conn.execute(text(sql)).all()
        for item in result:
            topic_name = item[0]
            count = item[1]
            statistics[topic_name]["characters"] = count

        sql = "SELECT topic, count(*) FROM relations GROUP BY topic"
        result = conn.execute(text(sql)).all()
        for item in result:
            topic_name = item[0]
            count = item[1]
            statistics[topic_name]["relations"] = count

        sql = "SELECT topic, count(DISTINCT group_name) FROM groupx GROUP BY topic"
        result = conn.execute(text(sql)).all()
        for item in result:
            topic_name = item[0]
            count = item[1]
            statistics[topic_name]["groups"] = count

        return_result = {
            "count": topic_count,
            "statistics": list(statistics.values())
        }

        conn.close()
        return return_result

    """
    Create one topic with name.
    """
    def create_topic(self, name: str) -> list:
        conn = self.engine.connect()
        sql = "INSERT INTO topics (name) VALUES (:name)"
        params = [{"name": name}]
        conn.execute(text(sql), params)
        conn.commit()
        conn.close()

    """
    Create one topic with name if not exists.
    """
    def create_topic_if_not_exist(self, name: str) -> list:
        conn = self.engine.connect()
        sql = "INSERT INTO topics (name) SELECT '{}' WHERE not exists (SELECT name FROM topics WHERE name='{}')".format(name, name)
        conn.execute(text(sql))
        conn.commit()
        conn.close()        

    """
    Delete one topic with name.
    """
    def delete_topic(self, topic_name: str) -> list:
        conn = self.engine.connect()
        sql = "DELETE FROM topics WHERE name='{}'".format(topic_name)
        conn.execute(text(sql))
        conn.commit()
        conn.close()

    """
    Get all characters from single topic.
    """
    def get_characters(self, topic: str, chosen_node_names: list = []) -> list:
        conn = self.engine.connect()
        if len(chosen_node_names) > 0:
            # If pass chosen nodes
            names_str = ",".join(["'{}'".format(name)
                                 for name in chosen_node_names])
            sql = "SELECT name, weight, note, image_name FROM characters WHERE topic = '{}' and name IN ({})".format(
                topic, names_str)
        else:
            sql = "SELECT name, weight, note, image_name FROM characters WHERE topic = '{}'".format(
                topic)

        result = conn.execute(text(sql)).all()

        conn.close()
        return [{"name": row[0], "weight": row[1], "note": row[2], "image_name": row[3]} for row in result]

    """
    Get character detail.
    """
    def get_character(self, topic: str, name: str) -> list:
        conn = self.engine.connect()
        sql = "SELECT name, weight, note, image_name FROM characters WHERE topic='{}' AND name='{}'".format(
            topic, name)
        result = conn.execute(text(sql))
        row = result.all()[0]

        conn.close()
        return {"name": row[0], "weight": row[1], "note": row[2], "image_name": row[3]}

    """
    Get characters names from some groups.
    """
    def get_characters_names(self, topic: str, chosen_groups: list) -> list:
        conn = self.engine.connect()
        if len(chosen_groups) > 0:
            group_str = ",".join(["'{}'".format(name)
                                 for name in chosen_groups])
            sql = "SELECT distinct(character_name) FROM groupx WHERE topic = '{}' and group_name IN ({})".format(
                topic, group_str)
        else:
            sql = "SELECT distinct(character_name) FROM groupx WHERE topic = '{}'".format(
                topic)

        result = conn.execute(text(sql)).all()

        conn.close()
        return [{"name": row[0], "weight": row[1], "note": row[2], "image_name": row[3]} for row in result]

    """
    Create one character. tobedev
    """
    def create_character(self, topic: str, name: str, note: str, image_name: str) -> None:
        conn = self.engine.connect()
        sql = "INSERT INTO characters (topic, name, note, image_name) VALUES ('{}', '{}', '{}', '{}')".format(
            topic, name, note, image_name)
        conn.execute(text(sql))
        conn.commit()
        conn.close()

    """
    Get relations from single topic.
    """
    def get_relations(self, topic: str) -> None:
        conn = self.engine.connect()
        sql = "SELECT source, target, relation, note FROM relations WHERE topic = '{}'".format(
            topic)
        result = conn.execute(text(sql)).all()

        conn.close()
        return [{"source": row[0], "target": row[1], "relation": row[2], "note": row[3]} for row in result]

    """
    Get groups from single topic.
    """
    def get_groups(self, topic: str) -> list:
        conn = self.engine.connect()
        sql = "SELECT group_name, character_name FROM groupx WHERE topic = '{}'".format(
            topic)
        result = conn.execute(text(sql)).all()

        conn.close()
        return [{"group_name": row[0], "character_name": row[1]} for row in result]

    """
    Get group_names from single topic.
    """
    def get_groups_names(self, topic: str) -> list:
        conn = self.engine.connect()
        sql = "SELECT distinct(group_name) FROM groupx WHERE topic = '{}'".format(
            topic)
        result = conn.execute(text(sql)).all()

        conn.close()
        return [row[0] for row in result]

    """
    Get characters names from some groups.
    """
    def get_characters_names_in_groups(self, topic: str, chosen_groups: list) -> list:
        conn = self.engine.connect()
        if len(chosen_groups) > 0:
            group_str = ",".join(["'{}'".format(name)
                                 for name in chosen_groups])
            sql = "SELECT distinct(character_name) FROM groupx WHERE topic = '{}' and group_name IN ({})".format(
                topic, group_str)
        else:
            sql = "SELECT distinct(character_name) FROM groupx WHERE topic = '{}'".format(
                topic)

        result = conn.execute(text(sql)).all()

        conn.close()
        return [row[0] for row in result]

    """
    Update characters table.
    """
    def update_characters(self, topic: str, insert_characters: list, update_characters: list, delete_characters: list) -> None:
        conn = self.engine.connect()

        if len(insert_characters) > 0:
            sql = "INSERT INTO characters (topic, name, note, image_name) VALUES ('{}', :name, :note, :image_name)".format(
                topic)
            params = [{"name": insert_character["name"], "note": insert_character["note"],
                       "image_name": insert_character["image_name"]} for insert_character in insert_characters]
            conn.execute(text(sql), params)

        if len(update_characters) > 0:
            sql = "UPDATE characters SET note=:note, image_name=:image_name WHERE topic='{}' AND name=:name".format(
                topic)
            params = [{"note": update_character["note"], "image_name": update_character["image_name"],
                       "name": update_character["name"]} for update_character in update_characters]
            conn.execute(text(sql), params)

        if len(delete_characters) > 0:
            sql = "DELETE FROM characters WHERE topic='{}' AND name=:name".format(
                topic)
            params = [{"name": delete_character["name"]}
                      for delete_character in delete_characters]
            conn.execute(text(sql), params)

        conn.commit()
        conn.close()

    """
    Create one relation.
    """
    def create_relation(self, topic: str, source: str, target: str, relation: str, note: str) -> None:
        conn = self.engine.connect()
        sql = "INSERT INTO relations (topic, source, target, relation, note) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            topic, source, target, relation, note)
        conn.execute(text(sql))
        conn.commit()
        conn.close()

    """
    Add upstream and downstream relations for single character.

    upstream_relations and downstream_relations should be like this:
    [
        {
            "character_name": "foo",
            "relation": "bar",
            "note": ""
        },
        {
            "character_name": "foo",
            "relation": "bar",
            "note": ""
        }
    ]
    """
    def add_relations_for_character(self, topic: str, character_name: str, upstream_relations: array, downstream_relations: array) -> None:
        conn = self.engine.connect()
        sql = "INSERT INTO relations (topic, source, target, relation, note) VALUES ('{}', :source, :target, :relation, :note)".format(
            topic)
        upstream_params = [{"source": upstream_relation["character_name"], "target": character_name,
                            "relation": upstream_relation["relation"], "note": upstream_relation["note"]} for upstream_relation in upstream_relations]
        downstream_params = [{"source": character_name, "target": downstream_relation["character_name"],
                              "relation": downstream_relation["relation"], "note": downstream_relation["note"]} for downstream_relation in downstream_relations]
        conn.execute(text(sql), upstream_params + downstream_params)
        conn.commit()
        conn.close()

    """
    Update relations table.
    """
    def update_relations(self, topic: str, insert_relations: list, update_relations: list, delete_relations: list) -> None:
        conn = self.engine.connect()

        if len(insert_relations) > 0:
            sql = "INSERT INTO relations (topic, source, target, relation, note) VALUES ('{}', :source, :target, :relation, :note)".format(
                topic)
            params = [{"source": insert_relation["source"], "target": insert_relation["target"],
                       "relation": insert_relation["relation"], "note": insert_relation["note"]
                       } for insert_relation in insert_relations]
            conn.execute(text(sql), params)

        if len(update_relations) > 0:
            sql = "UPDATE relations SET relation=:relation, note=:note WHERE topic='{}' AND source=:source AND target=:target".format(
                topic)
            params = [{"relation": update_relation["relation"], "note": update_relation["note"],
                       "source": update_relation["source"], "target": update_relation["target"]
                       } for update_relation in update_relations]
            conn.execute(text(sql), params)

        if len(delete_relations) > 0:
            sql = "DELETE FROM relations WHERE topic='{}' AND source=:source AND target=:target".format(
                topic)
            params = [{"source": delete_relation["source"], "target": delete_relation["target"]}
                      for delete_relation in delete_relations]
            conn.execute(text(sql), params)

        conn.commit()
        conn.close()

    """
    Create one group.
    """
    def create_group(self, topic: str, group_name: str, character_name: str) -> None:
        conn = self.engine.connect()
        sql = "INSERT INTO groupx (topic, group_name, character_name) VALUES ('{}', '{}', '{}')".format(
            topic, group_name, character_name)
        conn.execute(text(sql))
        conn.commit()
        conn.close()

    """
    Join the groups for single character.
    """
    def join_groups(self, topic: str, character_name: str, groups_names: array) -> None:
        conn = self.engine.connect()
        sql = "INSERT INTO groupx (topic, group_name, character_name) VALUES ('{}', :group_name, '{}')".format(
            topic, character_name)
        params = [{"group_name": group_name} for group_name in groups_names]
        conn.execute(text(sql), params)
        conn.commit()
        conn.close()

    """
    Update groupx table.
    """
    def update_groups(self, topic: str, insert_groups: list, update_groups: list, delete_groups: list) -> None:
        conn = self.engine.connect()

        if len(insert_groups) > 0:
            sql = "INSERT INTO groupx (topic, group_name, character_name) VALUES ('{}', :group_name, :character_name)".format(
                topic)
            params = [{"group_name": insert_group["group_name"],
                       "character_name": insert_group["character_name"]} for insert_group in insert_groups]
            conn.execute(text(sql), params)

        if len(delete_groups) > 0:
            sql = "DELETE FROM groupx WHERE topic='{}' AND group_name=:group_name AND character_name=:character_name".format(
                topic)
            params = [{"group_name": delete_group["group_name"],
                       "character_name": delete_group["character_name"]} for delete_group in delete_groups]
            conn.execute(text(sql), params)

        conn.commit()
        conn.close()

    """
    Compute character and character paths.
    """
    def compute_paths(self, topic: str, source: str, target: str, cutoff: int = -1, only_directed: bool = False) -> list:
        util = networkx_util.NetworkxUtil(self.engine, topic)
        # TODO: Add more info for front-end
        return util.get_all_path(source, target, cutoff, only_directed)

    """
    Get the upstream characters of single character.
    """
    def get_upstream_characters(self, topic: str, name: str) -> None:
        conn = self.engine.connect()
        sql = "SELECT name, weight, note, image_name FROM characters WHERE name in (SELECT source FROM relations WHERE topic='{}' AND target='{}')".format(
            topic, name)
        result = conn.execute(text(sql)).all()

        conn.close()
        return [{"name": row[0], "weight": row[1], "note": row[2], "image_name": row[3]} for row in result]

    """
    Get the downstream characters of single character.
    """
    def get_downstream_characters(self, topic: str, name: str) -> None:
        conn = self.engine.connect()
        sql = "SELECT name, weight, note, image_name FROM characters WHERE name in (SELECT target FROM relations WHERE topic='{}' AND source='{}')".format(
            topic, name)
        result = conn.execute(text(sql)).all()

        conn.close()
        return [{"name": row[0], "weight": row[1], "note": row[2], "image_name": row[3]} for row in result]

    """
    Update the characters weights from single topic.
    """
    def update_characters_weights(self, topic: str) -> None:
        util = networkx_util.NetworkxUtil(self.engine, topic)
        util.update_characters_weight()

    """
    Export one topic data to specified directory.
    """
    def export_topic(self, topic, export_dir="/tmp/"):
        print("Try to export topic: {}, to directory: {}".format(topic, export_dir))
        export_topic_dir = "{}/{}".format(export_dir, topic)
        conn = self.engine.connect()

        # Create directory recursively if not exists
        if not os.path.exists(export_topic_dir):
            os.makedirs(export_topic_dir)

        # Export characters
        export_file_path = export_topic_dir + "/characters.csv"
        sql = "SELECT * FROM characters WHERE topic='{}'".format(topic)
        DbService.excute_sql_export_csv(conn, sql, export_file_path)

        # Export relations
        export_file_path = export_topic_dir + "/relations.csv"
        sql = "SELECT * FROM relations WHERE topic='{}'".format(topic)
        DbService.excute_sql_export_csv(conn, sql, export_file_path)

        # Export groups
        export_file_path = export_topic_dir + "/groups.csv"
        sql = "SELECT * FROM groupx WHERE topic='{}'".format(topic)
        DbService.excute_sql_export_csv(conn, sql, export_file_path)

        # Export image files
        source_image_path = "./dist/images/" + topic
        target_image_path = export_topic_dir + "/images/"
        if os.path.exists(export_topic_dir):
            logging.warn("Image path of {} exists, remove first".format(target_image_path))
            shutil.rmtree(target_image_path)
        shutil.copytree(source_image_path, target_image_path)

        conn.close()

    """
    Execute SQL and export result to CSV file.
    """
    @staticmethod
    def excute_sql_export_csv(connection, sql: str , csv_file_path: str) -> None:
        # Execute SQL
        result = connection.execute(text(sql))

        # Create CSV file
        outfile = open(csv_file_path, 'w')
        csv_writer = csv.writer(outfile)

        # Write header
        csv_writer.writerow(x[0] for x in result.cursor.description)
        # Write data
        csv_writer.writerows(result.cursor.fetchall())

    """
    Load one topic data from specified directory.
    """
    def import_topic(self, topic, import_dir="/tmp/"):
        print("Try to import topic: {}, from directory: {}".format(topic, import_dir))
        import_topic_dir = "{}{}".format(import_dir, topic)


        # Check if directory exists or not
        if not os.path.exists(import_topic_dir):
            logging.error("Import path of {} does not exit, exit now")
            return

        # Create topic if not exists
        self.create_topic_if_not_exist(topic)

        # Load data from csv files to tables
        DbService.load_csv_to_table(import_topic_dir + "/characters.csv", self.engine, "characters")
        DbService.load_csv_to_table(import_topic_dir + "/relations.csv", self.engine, "relations")
        DbService.load_csv_to_table(import_topic_dir + "/groups.csv", self.engine, "groupx")

        # Copy image files to dist
        source_image_path = import_topic_dir + "/images/"
        target_image_path = "./dist/images/" + topic
        files = os.listdir(source_image_path)
        for fname in files:
            shutil.copy2(os.path.join(source_image_path, fname), target_image_path)

    """
    Load CSV file to table of database.
    """
    @staticmethod
    def load_csv_to_table(csv_path: str, engine, table_name: str) -> None:
        with open(csv_path, 'r') as file:
            data_df = pd.read_csv(file)
            data_df.to_sql(table_name, con=engine, index=False, if_exists='replace')


if __name__ == "__main__":
    #service = DbService(DbConfig.create_default_config())
    #service.export_topic("赛博朋克：边缘行者")
    
    #service = DbService(DbConfig("mysql", "127.0.0.1:3306", "root", "root", "graph_book"))
    #service.import_topic("赛博朋克：边缘行者")
