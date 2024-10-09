import mysql.connector
from flask import current_app


def get_db_connection():
    db_config = current_app.config['db_config']
    conn = mysql.connector.connect(**db_config)
    return conn


# 删除 Redis 的导入和相关代码
# import redis

# 删除 get_redis_connection 函数
# def get_redis_connection():
#     redis_config = current_app.config['redis_config']
#     r = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'], db=redis_config['db'])
#     return r

