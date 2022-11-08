from array import array
import pymysql.cursors
import logging

import model
import networkx_util

logging.basicConfig(level=logging.INFO)


class DbService(object):
    def __init__(self) -> None:
        pass

    def get_nodes_for_frontend(self, db_config: model.DbConfig, db: str, limit_num: int=-1, group_name: str="", chosen_node_names: list=[]) -> list:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            # If pass chosen nodes
            if len(chosen_node_names) > 0:
                # Generate the SQL parameter, for example: "'kiwi','pilar','rebecca'"
                names_str = ",".join(["'{}'".format(name) for name in chosen_node_names])
                sql = "SELECT id as row_id, name, display_name, note, weight FROM {}.nodes WHERE name IN ({})".format(db, names_str)                
                print("Try to execute sql: {}".format(sql))
                cursor.execute(sql)
                result_set = cursor.fetchall()
                return result_set
            else:
                sql = "SELECT id as row_id, name, display_name, note, weight FROM {}.nodes".format(db)

                if group_name != "":
                    sql += " WHERE name IN (SELECT node_name FROM teams WHERE group_name = '{}')".format(group_name)

                if limit_num > 0:
                    sql = sql + " ORDER BY id LIMIT {}".format(limit_num)

                
                    chosen_nodes
                    sql += " IN ()"
                
                print("Try to execute sql: {}".format(sql))
                cursor.execute(sql)
                result_set = cursor.fetchall()
                return result_set

    def get_node_downstream(self, db_config: model.DbConfig, db: str, node_name: str) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            sql = "SELECT * FROM {}.nodes WHERE name in (SELECT target FROM edges WHERE source = %s)".format(db)
            print("Try to execute sql: {}".format(sql))
            cursor.execute(sql, node_name)
            result_set = cursor.fetchall()
            return result_set

    def get_node_upstream(self, db_config: model.DbConfig, db: str, node_name: str) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            sql = "SELECT * FROM {}.nodes WHERE name in (SELECT source FROM edges WHERE target = %s)".format(db)
            print("Try to execute sql: {}".format(sql))
            cursor.execute(sql, node_name)
            result_set = cursor.fetchall()
            return result_set

    def update_nodes_weight(self, db_config: model.DbConfig, db: str) -> None:
        util = networkx_util.NetworkxUtil(db_config, db)
        util.update_wight()


    def get_edges_for_frontend(self, db_config: model.DbConfig, db: str) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            sql = "SELECT * FROM {}.edges".format(db)
            cursor.execute(sql)
            result_set = cursor.fetchall()
            return result_set

    def get_groups_for_frontend(self, db_config: model.DbConfig, db: str) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            sql = "SELECT * FROM {}.teams".format(db)
            cursor.execute(sql)
            result_set = cursor.fetchall()
            return result_set

    def get_group_names(self, db_config: model.DbConfig, db: str) -> array:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            sql = "SELECT distinct(group_name) FROM {}.teams".format(db)
            cursor.execute(sql)
            result_set = cursor.fetchall()
            group_names = [row["group_name"] for row in result_set]
            return group_names

    def update_nodes(self, db_config: model.DbConfig, db: str, insert_nodes: array, update_nodes: array, delete_nodes: array) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            if len(insert_nodes) > 0:
                sql = "INSERT INTO {}.nodes (name, display_name, note) VALUES (%s, %s, %s)".format(db);
                insert_nodes_data = [(insert_node["name"], insert_node["display_name"], insert_node["note"]) for insert_node in insert_nodes]
                print("Try to execute sql: {}, data: {}".format(sql, insert_nodes_data))
                cursor.executemany(sql, insert_nodes_data)

            for update_node in update_nodes:
                sql = "UPDATE {}.nodes SET display_name=%s, note=%s WHERE name=%s".format(db)
                update_nodes_data = (update_node["display_name"], update_node["note"], update_node["name"])
                print("Try to execute sql: {}, data: {}".format(sql, update_nodes_data))
                cursor.execute(sql, update_nodes_data)

            if len(delete_nodes) > 0:
                sql = "DELETE FROM {}.nodes WHERE name=%s".format(db);
                delete_nodes_data = [(delete_node["name"]) for delete_node in delete_nodes]
                print("Try to execute sql: {}, data: {}".format(sql, delete_nodes_data))
                cursor.executemany(sql, delete_nodes_data)

        connection.commit()

    def update_edges(self, db_config: model.DbConfig, db: str, insert_edges: array, update_edges: array, delete_edges: array) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            if len(insert_edges) > 0:
                sql = "INSERT INTO {}.edges (source, target, relation, note) VALUES (%s, %s, %s, %s)".format(db);
                insert_edges_data = [(insert_edge["source"], insert_edge["target"], insert_edge["relation"], insert_edge["note"]) for insert_edge in insert_edges]
                print("Try to execute sql: {}, data: {}".format(sql, insert_edges_data))
                cursor.executemany(sql, insert_edges_data)

            for update_edge in update_edges:
                sql = "UPDATE {}.edges SET relation=%s, note=%s WHERE source=%s AND target=%s".format(db)
                update_edges_data = (update_edge["relation"], update_edge["note"], update_edge["source"], update_edge["target"])
                print("Try to execute sql: {}, data: {}".format(sql, update_edges_data))
                cursor.execute(sql, update_edges_data)

            if len(delete_edges) > 0:
                sql = "DELETE FROM {}.edges WHERE source=%s AND target=%s".format(db);
                delete_edges_data = [(delete_edge["source"], delete_edge["target"]) for delete_edge in delete_edges]
                print("Try to execute sql: {}, data: {}".format(sql, delete_edges_data))
                cursor.executemany(sql, delete_edges_data)

        connection.commit()

    def update_groups(self, db_config: model.DbConfig, db: str, insert_groups: array, update_groups: array, delete_groups: array) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            if len(insert_groups) > 0:
                sql = "INSERT INTO {}.teams (group_name, node_name) VALUES (%s, %s)".format(db);
                insert_groups_data = [(insert_group["group_name"], insert_group["node_name"]) for insert_group in insert_groups]
                print("Try to execute sql: {}, data: {}".format(sql, insert_groups_data))
                cursor.executemany(sql, insert_groups_data)

            for update_group in update_groups:
                sql = "UPDATE {}.teams SET group_name=%s, node_name=%s WHERE id=%s".format(db)
                update_groups_data = (update_group["group_name"], update_group["node_name"], update_group["id"])
                print("Try to execute sql: {}, data: {}".format(sql, update_groups_data))
                cursor.execute(sql, update_groups_data)

            if len(delete_groups) > 0:
                sql = "DELETE FROM {}.teams WHERE id=%s".format(db);
                delete_groups_data = [(delete_group["id"]) for delete_group in delete_groups]
                print("Try to execute sql: {}, data: {}".format(sql, delete_groups_data))
                cursor.executemany(sql, delete_groups_data)

        connection.commit()

    def get_node_node_paths(self, db_config: model.DbConfig, db: str, source: str, target, str, cutoff: int=-1) -> None:
        util = networkx_util.NetworkxUtil(db_config, db)
        # TODO: Add more info for front-end
        return util.get_all_path(source, target, cutoff)

def main():
    db_config = model.DbConfig("localhost", "root", "wawa316", "cyberpunk_edgerunner")
    graph = model.Graph()
    graph.load_from_db(db_config, "cyberpunk_edgerunner")

    db_service = DbService()
    print(graph)


if __name__ == "__main__":
    main()


