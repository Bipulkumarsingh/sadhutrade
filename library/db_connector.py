from pymongo import MongoClient


# client = MongoClient('localhost', 27017)
client = MongoClient("mongodb://localhost:27017/?authSource=local").get_database("local")
print(client.list_collection_names())

# import os
# import json
# from src.logger import set_up_logging
#
# logger = set_up_logging()
#
#
# def mongo_db_connect() -> object:
#     try:
#         file_name = get_configuration_filename()
#         if not os.path.isfile(file_name):
#             config = {'host': os.environ.get('dbhost', None), 'database': os.environ.get('database', None)}
#             if config['host'] is None:
#                 return None
#         else:
#             with open(file_name) as _f:
#                 config = json.load(_f)['parameters'].get('mongodb', None)
#                 if config is None:
#                     return None
#         host = config['host']
#         port = config.get('port', 27017)
#         username = config.get('username', config.get('user', None))
#         password = config.get('password', None)
#         database = config.pop('database', 'doyouknow')
#
#         _mongodb_url = f"{host}:{port}/?authSource={database}"
#
#         if username is None:
#             mongodb_url = f"mongodb://{_mongodb_url}"
#         else:
#             mongodb_url = f"mongodb://{username}:{password}@{_mongodb_url}&authMechanism=SCRAM-SHA-256"
#
#         from pymongo import MongoClient
#         from pymongo.database import Database
#
#         db: Database = MongoClient(mongodb_url).get_database(database)
#         return db
#     except Exception as ex:
#         logger.error(f'Error: {str(ex)}')
#         raise Exception(f'Issue with MongoDB credential: {str(ex)}')
